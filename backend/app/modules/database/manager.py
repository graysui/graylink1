"""
数据库管理器模块
提供数据库操作的高级接口
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, event
from sqlalchemy.sql import text
from typing import List, Optional, Dict, Type, TypeVar
from datetime import datetime, timedelta
from loguru import logger
from contextlib import asynccontextmanager
import time
from ...core.cache import cached, cache
from ...core.base import BaseModel
from ...core.session import session_manager
from ..monitor.models import FileRecord
from ...core.config import settings

T = TypeVar('T', bound=BaseModel)

class DatabaseManager:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.batch_size = settings.database.batch_size
        self.stats = {
            "queries": 0,
            "updates": 0,
            "errors": 0,
            "last_error": None,
            "slow_queries": []
        }

    @asynccontextmanager
    async def transaction(self):
        """事务上下文管理器，使用会话管理器"""
        async with session_manager.session() as session:
            try:
                self.session = session
                yield
            except Exception as e:
                self.stats["errors"] += 1
                self.stats["last_error"] = str(e)
                raise

    async def _record_query_time(self, operation: str, start_time: float, query: str):
        """记录查询时间"""
        duration = time.time() - start_time
        if duration > 1.0:  # 记录超过1秒的慢查询
            self.stats["slow_queries"].append({
                "query": query,
                "duration": duration,
                "timestamp": datetime.now().isoformat()
            })
            logger.warning(f"慢查询 ({duration:.2f}s): {query}")

    async def get_by_id(self, model: Type[T], id: int) -> Optional[T]:
        """通用的通过 ID 获取记录方法"""
        try:
            start_time = time.time()
            self.stats["queries"] += 1
            
            result = await self.session.get(model, id)
            
            await self._record_query_time("select", start_time, f"Get {model.__name__} by id {id}")
            return result
        except Exception as e:
            logger.error(f"获取记录失败: {str(e)}")
            raise

    @cached(prefix="file", ttl=300)
    async def get_file_by_id(self, file_id: str) -> Optional[FileRecord]:
        """获取单个文件记录（使用缓存）"""
        try:
            start_time = time.time()
            self.stats["queries"] += 1
            
            stmt = select(FileRecord).where(FileRecord.file_id == file_id)
            result = await self.session.execute(stmt)
            record = result.scalar_one_or_none()
            
            await self._record_query_time("select", start_time, str(stmt))
            return record
        except Exception as e:
            logger.error(f"获取文件记录失败: {str(e)}")
            raise

    @cached(prefix="files", ttl=60)
    async def get_files_by_path(self, path: str) -> List[FileRecord]:
        """获取指定路径下的文件记录（优化查询）"""
        try:
            start_time = time.time()
            self.stats["queries"] += 1
            
            stmt = (
                select(FileRecord)
                .where(FileRecord.path.like(f"{path}%"))
                .order_by(FileRecord.path)
            )
            result = await self.session.execute(stmt)
            records = result.scalars().all()
            
            await self._record_query_time("select", start_time, str(stmt))
            return records
        except Exception as e:
            logger.error(f"获取路径下的文件记录失败: {str(e)}")
            raise

    async def get_database_stats(self) -> Dict:
        """获取数据库统计信息"""
        try:
            # 基本统计
            result = await self.session.execute(
                select(
                    func.count(FileRecord.id).label('total_records'),
                    func.sum(FileRecord.size).label('total_size'),
                    func.count(FileRecord.id).filter(FileRecord.is_directory).label('directories')
                )
            )
            stats = result.first()
            
            # 性能统计
            performance_stats = {
                "query_count": self.stats["queries"],
                "update_count": self.stats["updates"],
                "error_count": self.stats["errors"],
                "last_error": self.stats["last_error"],
                "slow_queries": self.stats["slow_queries"][-5:],  # 最近5个慢查询
                "cache_stats": cache.get_stats(),
                "session_stats": session_manager.get_stats()
            }
            
            return {
                "database": {
                    "total_records": stats.total_records or 0,
                    "total_size": stats.total_size or 0,
                    "directories": stats.directories or 0
                },
                "performance": performance_stats
            }
        except Exception as e:
            logger.error(f"获取数据库统计信息失败: {str(e)}")
            raise

    async def update_file_records(self, records: List[Dict]) -> Dict[str, int]:
        """批量更新文件记录"""
        try:
            updated = 0
            inserted = 0
            
            # 分批处理更新
            for i in range(0, len(records), self.batch_size):
                batch = records[i:i + self.batch_size]
                
                # 获取现有记录
                file_ids = [r['file_id'] for r in batch]
                existing = await self.session.execute(
                    select(FileRecord)
                    .where(FileRecord.file_id.in_(file_ids))
                )
                existing_map = {
                    r.file_id: r for r in existing.scalars().all()
                }
                
                # 更新或插入记录
                for record in batch:
                    if record['file_id'] in existing_map:
                        # 更新现有记录
                        existing_record = existing_map[record['file_id']]
                        for key, value in record.items():
                            setattr(existing_record, key, value)
                        updated += 1
                    else:
                        # 插入新记录
                        self.session.add(FileRecord(**record))
                        inserted += 1
                
                await self.session.flush()
            
            await self.session.commit()
            return {"updated": updated, "inserted": inserted}
            
        except Exception as e:
            await self.session.rollback()
            logger.error(f"更新文件记录失败: {str(e)}")
            raise

    async def optimize_database(self):
        """优化数据库（增加更多优化操作）"""
        try:
            # 对于SQLite
            await self.session.execute(text("VACUUM"))
            await self.session.execute(text("ANALYZE"))
            
            # 更新统计信息
            await self.session.execute(text("ANALYZE file_records"))
            
            # 重建索引
            await self.session.execute(text("REINDEX"))
            
            await self.session.commit()
            logger.info("数据库优化完成")
        except Exception as e:
            logger.error(f"数据库优化失败: {str(e)}")
            raise 
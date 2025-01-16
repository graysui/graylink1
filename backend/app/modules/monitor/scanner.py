"""文件扫描模块

提供文件系统扫描和变更检测功能。
"""
from datetime import datetime, timedelta
import os
from typing import List, Dict, Optional, Set
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.future import select as future_select
from app.core.cache import cached
from app.core.config import settings

from .models import FileRecord
from .gdrive import GoogleDriveClient

class FileScanner:
    """文件扫描器
    
    负责扫描目录并检测文件变更。
    """
    
    def __init__(self, db_session: AsyncSession, gdrive_client: GoogleDriveClient):
        """初始化扫描器
        
        Args:
            db_session: 数据库会话
            gdrive_client: Google Drive 客户端
        """
        self.db_session = db_session
        self.gdrive_client = gdrive_client
        self._scan_count = 0
        self._last_scan_time = None
        self._last_scan_duration = None
        
    @property
    def stats(self) -> Dict:
        """获取扫描统计信息"""
        return {
            "total_scans": self._scan_count,
            "last_scan_time": self._last_scan_time.isoformat() if self._last_scan_time else None,
            "last_scan_duration": self._last_scan_duration
        }
        
    async def scan_directory(self, directory: str) -> List[Dict]:
        """扫描目录并返回变更
        
        Args:
            directory: 要扫描的目录路径
            
        Returns:
            变更列表，每个变更包含类型和文件信息
        """
        start_time = datetime.now()
        self._scan_count += 1
        self._last_scan_time = start_time
        
        try:
            changes = []
            
            # 获取目录下所有文件
            files = await self.gdrive_client.list_files(directory)
            current_file_ids = {f['id'] for f in files}
            
            # 批量检查现有记录
            existing_records = await self._get_existing_records(current_file_ids)
            existing_file_ids = {record.file_id for record in existing_records}
            
            # 处理新文件和修改的文件
            for file in files:
                try:
                    modified_time = datetime.fromisoformat(
                        file['modifiedTime'].replace('Z', '+00:00')
                    )
                    
                    existing_record = next(
                        (r for r in existing_records if r.file_id == file['id']),
                        None
                    )
                    
                    if not existing_record:
                        # 新文件
                        changes.append({
                            'type': 'added',
                            'file': file
                        })
                        await self._create_file_record(file, modified_time)
                    elif existing_record.modified_time < modified_time:
                        # 文件已修改
                        changes.append({
                            'type': 'modified',
                            'file': file
                        })
                        await self._update_file_record(existing_record, file, modified_time)
                    
                except Exception as e:
                    logger.error(f"处理文件出错 [{file.get('name', 'unknown')}]: {str(e)}")
                    continue
            
            # 检查删除的文件
            deleted_files = await self._find_deleted_files(directory, current_file_ids)
            changes.extend(deleted_files)
            
            # 提交更改
            await self.db_session.commit()
            
            # 更新统计信息
            self._last_scan_duration = (datetime.now() - start_time).total_seconds()
            
            return changes
            
        except Exception as e:
            logger.error(f"扫描目录出错 [{directory}]: {str(e)}")
            await self.db_session.rollback()
            raise
            
        finally:
            # 清理过期的缓存记录
            await self._cleanup_expired_records()

    @cached(prefix="file_scanner", ttl=60)
    async def _get_existing_records(self, file_ids: Set[str]) -> List[FileRecord]:
        """获取现有文件记录
        
        Args:
            file_ids: 文件ID集合
            
        Returns:
            文件记录列表
        """
        result = await self.db_session.execute(
            select(FileRecord).where(FileRecord.file_id.in_(file_ids))
        )
        return result.scalars().all()

    async def _create_file_record(self, file: Dict, modified_time: datetime):
        """创建新的文件记录
        
        Args:
            file: 文件信息
            modified_time: 修改时间
        """
        # 构建相对路径
        relative_path = file['name']  # Google Drive API 返回的路径
        
        record = FileRecord(
            file_id=file['id'],
            path=relative_path,
            modified_time=modified_time,
            size=int(file.get('size', 0)),
            is_directory=file['mimeType'] == 'application/vnd.google-apps.folder',
            mime_type=file['mimeType']
        )
        self.db_session.add(record)

    async def _update_file_record(self, record: FileRecord, file: Dict, modified_time: datetime):
        """更新现有文件记录
        
        Args:
            record: 现有记录
            file: 新的文件信息
            modified_time: 修改时间
        """
        record.modified_time = modified_time
        record.size = int(file.get('size', 0))
        record.path = file['name']
        record.mime_type = file['mimeType']

    async def _find_deleted_files(self, directory: str, current_file_ids: Set[str]) -> List[Dict]:
        """查找已删除的文件
        
        Args:
            directory: 目录路径
            current_file_ids: 当前文件ID集合
            
        Returns:
            删除的文件列表
        """
        # 查询数据库中的所有文件记录
        result = await self.db_session.execute(
            select(FileRecord).where(
                and_(
                    FileRecord.path.like(f"{directory}/%"),
                    FileRecord.file_id.notin_(current_file_ids)
                )
            )
        )
        db_records = result.scalars().all()
        
        deleted_files = []
        for record in db_records:
            deleted_files.append({
                'type': 'deleted',
                'file': record.to_dict()
            })
            await self.db_session.delete(record)
                
        return deleted_files

    async def _cleanup_expired_records(self):
        """清理过期的记录"""
        try:
            # 删除超过30天未检查的记录
            cutoff_date = datetime.utcnow() - timedelta(days=30)
            await self.db_session.execute(
                FileRecord.__table__.delete().where(
                    FileRecord.last_checked < cutoff_date
                )
            )
            await self.db_session.commit()
        except Exception as e:
            logger.error(f"清理过期记录失败: {str(e)}")
            await self.db_session.rollback() 
from datetime import datetime
import os
from typing import List, Dict, Optional
from loguru import logger
from .models import FileRecord
from .gdrive import GoogleDriveClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

class FileScanner:
    def __init__(self, db_session: AsyncSession, gdrive_client: GoogleDriveClient):
        self.db_session = db_session
        self.gdrive_client = gdrive_client
        
    async def scan_directory(self, directory: str) -> List[Dict]:
        """扫描目录并返回变更"""
        try:
            changes = []
            
            # 获取目录下所有文件
            files = await self.gdrive_client.list_files(directory)
            
            for file in files:
                # 检查文件是否存在于数据库
                existing_record = await self._get_file_record(file['id'])
                
                modified_time = datetime.fromisoformat(
                    file['modifiedTime'].replace('Z', '+00:00')
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
                
                # 更新最后检查时间
                existing_record.last_checked = datetime.utcnow()
                
            # 检查删除的文件
            deleted_files = await self._find_deleted_files(directory, files)
            changes.extend(deleted_files)
            
            await self.db_session.commit()
            return changes
            
        except Exception as e:
            logger.error(f"Error scanning directory: {str(e)}")
            await self.db_session.rollback()
            raise

    async def _get_file_record(self, file_id: str) -> Optional[FileRecord]:
        """从数据库获取文件记录"""
        result = await self.db_session.execute(
            select(FileRecord).where(FileRecord.file_id == file_id)
        )
        return result.scalar_one_or_none()

    async def _create_file_record(self, file: Dict, modified_time: datetime):
        """创建新的文件记录"""
        # 构建相对路径
        relative_path = file['name']  # Google Drive API 返回的路径
        
        record = FileRecord(
            file_id=file['id'],
            path=relative_path,  # 存储相对路径
            modified_time=modified_time,
            size=int(file.get('size', 0)),
            is_directory=file['mimeType'] == 'application/vnd.google-apps.folder'
        )
        self.db_session.add(record)

    async def _update_file_record(self, record: FileRecord, file: Dict, modified_time: datetime):
        """更新现有文件记录"""
        record.modified_time = modified_time
        record.size = int(file.get('size', 0))
        record.path = file['name']

    async def _find_deleted_files(self, directory: str, current_files: List[Dict]) -> List[Dict]:
        """查找已删除的文件"""
        current_file_ids = {f['id'] for f in current_files}
        
        # 查询数据库中的所有文件记录
        result = await self.db_session.execute(
            select(FileRecord).where(FileRecord.path.like(f"{directory}/%"))
        )
        db_records = result.scalars().all()
        
        deleted_files = []
        for record in db_records:
            if record.file_id not in current_file_ids:
                deleted_files.append({
                    'type': 'deleted',
                    'file': record.to_dict()
                })
                await self.db_session.delete(record)
                
        return deleted_files 
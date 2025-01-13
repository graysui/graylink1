from typing import List, Dict
from loguru import logger
from ..symlink.manager import SymlinkManager
from ..emby.service import EmbyService
from ...core.config import settings

class FileChangeHandler:
    def __init__(self):
        self.symlink_manager = SymlinkManager()
        self.emby_service = EmbyService()
        self.changed_paths = []  # 记录变更的路径

    async def handle_changes(self, changes: List[Dict]):
        """处理文件变更事件"""
        self.changed_paths = []  # 重置变更路径列表
        
        for change in changes:
            try:
                if change['type'] == 'added':
                    await self._handle_add(change['file'])
                elif change['type'] == 'modified':
                    await self._handle_modify(change['file'])
                elif change['type'] == 'deleted':
                    await self._handle_delete(change['file'])
            except Exception as e:
                logger.error(f"处理变更出错：{str(e)}")

        # 批量刷新变更的路径
        if self.changed_paths:
            try:
                result = await self.emby_service.refresh_by_paths(self.changed_paths)
                logger.info(f"Emby刷新结果：成功{result['success']}个，失败{result['failed']}个")
                if result['processed']:
                    logger.info(f"处理的媒体库路径：{', '.join(result['processed'])}")
            except Exception as e:
                logger.error(f"刷新Emby出错：{str(e)}")

    async def _handle_add(self, file: Dict):
        """处理文件添加"""
        if await self.symlink_manager.create_symlink(file['name']):
            self.changed_paths.append(file['name'])

    async def _handle_modify(self, file: Dict):
        """处理文件修改"""
        # 软链接不需要特殊处理，但可能需要刷新 Emby
        self.changed_paths.append(file['name'])

    async def _handle_delete(self, file: Dict):
        """处理文件删除"""
        if await self.symlink_manager.remove_symlink(file['path']):
            self.changed_paths.append(file['path']) 
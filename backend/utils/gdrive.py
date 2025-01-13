import logging
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os
import json
from datetime import datetime, timedelta
from typing import Optional, Dict, List
import requests

logger = logging.getLogger(__name__)

SCOPES = [
    'https://www.googleapis.com/auth/drive.readonly',
    'https://www.googleapis.com/auth/drive.metadata.readonly',
    'https://www.googleapis.com/auth/drive.activity.readonly'
]

class GoogleDriveAPI:
    def __init__(self, client_id: str, client_secret: str, token_file: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_file = token_file
        self.creds = None
        self._load_credentials()
        
    def get_file_path(self, file_id: str) -> Optional[str]:
        """获取文件的完整路径"""
        try:
            service = build('drive', 'v3', credentials=self.creds)
            file = service.files().get(
                fileId=file_id,
                fields='name,parents,mimeType'
            ).execute()
            
            path_parts = [file['name']]
            parent_id = file.get('parents', [None])[0]
            
            while parent_id:
                parent = service.files().get(
                    fileId=parent_id,
                    fields='name,parents'
                ).execute()
                path_parts.append(parent['name'])
                parent_id = parent.get('parents', [None])[0]
            
            return '/'.join(reversed(path_parts))
            
        except Exception as e:
            logger.error(f"获取文件路径失败: {str(e)}")
            return None

    def get_activities(self, folder_id: str, time_filter: str = "1h") -> List[Dict]:
        """获取文件活动
        
        Args:
            folder_id: 要监控的文件夹ID
            time_filter: 时间过滤，如 "1h", "1d", "7d"
        """
        service = build('driveactivity', 'v2', credentials=self.creds)
        
        # 计算时间范围
        now = datetime.utcnow()
        if time_filter.endswith('h'):
            start_time = now - timedelta(hours=int(time_filter[:-1]))
        elif time_filter.endswith('d'):
            start_time = now - timedelta(days=int(time_filter[:-1]))
        
        # 构建查询
        query = {
            'ancestorName': f'items/{folder_id}',
            'filter': f'time >= "{start_time.isoformat()}Z"'
        }
        
        try:
            results = []
            page_token = None
            while True:
                response = service.activity().query(body=query).execute()
                activities = response.get('activities', [])
                
                for activity in activities:
                    # 只关注创建和修改操作
                    if self._is_relevant_activity(activity):
                        parsed = self._parse_activity(activity)
                        if parsed:
                            # 获取文件完整路径
                            file_path = self.get_file_path(parsed['file']['id'])
                            if file_path:
                                parsed['file']['path'] = file_path
                                results.append(parsed)
                
                page_token = response.get('nextPageToken')
                if not page_token:
                    break
                query['pageToken'] = page_token
                
            return results
            
        except Exception as e:
            raise Exception(f"获取活动失败: {str(e)}")

    def _is_relevant_activity(self, activity: dict) -> bool:
        """判断是否是相关的活动"""
        if not activity.get('primaryActionDetail'):
            return False
            
        action = activity['primaryActionDetail']
        # 只关注文件创建、编辑和移动操作
        return any(key in action for key in ['create', 'edit', 'move'])

    def _parse_activity(self, activity: dict) -> Optional[Dict]:
        """解析活动信息"""
        action = activity['primaryActionDetail']
        targets = activity.get('targets', [])
        
        if not targets:
            return None
            
        target = next((t for t in targets if 'driveItem' in t), None)
        if not target:
            return None
            
        drive_item = target['driveItem']
        return {
            'action_type': next(iter(action.keys())),
            'time': activity['timestamp'],
            'file': {
                'id': drive_item.get('name', '').split('/')[-1],
                'title': drive_item.get('title', ''),
                'mime_type': drive_item.get('mimeType', '')
            }
        } 

    def get_auth_url(self) -> str:
        """获取授权URL"""
        flow = InstalledAppFlow.from_client_config(
            {
                "installed": {
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "redirect_uris": [
                        "http://localhost:8088/oauth2callback"  # 本地回调服务器
                    ],
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token"
                }
            },
            SCOPES
        )
        # 使用离线访问模式
        auth_url, _ = flow.authorization_url(
            access_type='offline',
            prompt='consent'  # 强制显示同意页面以获取refresh_token
        )
        return auth_url

    async def handle_oauth_callback(self, code: str) -> None:
        """处理OAuth回调"""
        flow = InstalledAppFlow.from_client_config(
            {
                "installed": {
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "redirect_uris": ["http://localhost:8088/oauth2callback"],
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token"
                }
            },
            SCOPES
        )
        flow.fetch_token(code=code)
        self.creds = flow.credentials
        self._save_credentials() 

    def get_device_code(self) -> dict:
        """获取设备码"""
        response = requests.post(
            'https://oauth2.googleapis.com/device/code',
            data={
                'client_id': self.client_id,
                'scope': 'https://www.googleapis.com/auth/drive.readonly'
            }
        )
        if response.status_code != 200:
            raise Exception('获取设备码失败')
        return response.json()

    def poll_token(self, device_code: str) -> dict:
        """轮询获取令牌"""
        response = requests.post(
            'https://oauth2.googleapis.com/token',
            data={
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'device_code': device_code,
                'grant_type': 'urn:ietf:params:oauth:grant-type:device_code'
            }
        )
        if response.status_code != 200:
            return None
        return response.json()

    def save_token(self, token_data: dict) -> None:
        """保存令牌"""
        token_info = {
            'token': token_data['access_token'],
            'refresh_token': token_data.get('refresh_token'),
            'token_uri': "https://oauth2.googleapis.com/token",
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'scopes': ['https://www.googleapis.com/auth/drive.readonly']
        }
        os.makedirs(os.path.dirname(self.token_file), exist_ok=True)
        with open(self.token_file, 'w') as f:
            json.dump(token_info, f)
        self.creds = Credentials.from_authorized_user_info(token_info) 
import os
import json
import logging
from typing import Dict, List, Optional
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class GoogleDriveAPI:
    def __init__(self, client_id: str, client_secret: str, token_file: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_file = token_file
        self.creds = None
        self._load_credentials()
        
    def _load_credentials(self):
        """加载凭证"""
        if os.path.exists(self.token_file):
            with open(self.token_file, 'r') as token:
                token_data = json.load(token)
                self.creds = Credentials.from_authorized_user_info(token_data)
                
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
                self._save_credentials()
                
    def _save_credentials(self):
        """保存凭证"""
        if self.creds:
            token_data = {
                'token': self.creds.token,
                'refresh_token': self.creds.refresh_token,
                'token_uri': self.creds.token_uri,
                'client_id': self.creds.client_id,
                'client_secret': self.creds.client_secret,
                'scopes': self.creds.scopes
            }
            os.makedirs(os.path.dirname(self.token_file), exist_ok=True)
            with open(self.token_file, 'w') as token:
                json.dump(token_data, token)
                
    def get_auth_url(self) -> str:
        """获取授权URL"""
        flow = InstalledAppFlow.from_client_config(
            {
                'installed': {
                    'client_id': self.client_id,
                    'client_secret': self.client_secret,
                    'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
                    'token_uri': 'https://oauth2.googleapis.com/token',
                }
            },
            ['https://www.googleapis.com/auth/drive.readonly']
        )
        auth_url, _ = flow.authorization_url(access_type='offline', include_granted_scopes='true')
        return auth_url
        
    def authorize_with_code(self, code: str) -> bool:
        """使用授权码完成授权"""
        try:
            flow = InstalledAppFlow.from_client_config(
                {
                    'installed': {
                        'client_id': self.client_id,
                        'client_secret': self.client_secret,
                        'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
                        'token_uri': 'https://oauth2.googleapis.com/token',
                    }
                },
                ['https://www.googleapis.com/auth/drive.readonly']
            )
            flow.fetch_token(code=code)
            self.creds = flow.credentials
            self._save_credentials()
            return True
        except Exception as e:
            logger.error(f"授权失败: {str(e)}")
            return False
            
    def list_files(self, folder_id: Optional[str] = None) -> List[Dict]:
        """列出文件"""
        if not self.creds:
            raise Exception("未授权")
            
        service = build('drive', 'v3', credentials=self.creds)
        query = f"'{folder_id}' in parents" if folder_id else None
        
        try:
            results = service.files().list(
                q=query,
                pageSize=100,
                fields="files(id, name, mimeType, modifiedTime)"
            ).execute()
            
            return results.get('files', [])
        except Exception as e:
            logger.error(f"列出文件失败: {str(e)}")
            return []
            
    def get_changes(self, start_time: Optional[datetime] = None) -> List[Dict]:
        """获取文件变更"""
        if not self.creds:
            raise Exception("未授权")
            
        service = build('drive', 'v3', credentials=self.creds)
        
        try:
            # 如果没有指定开始时间，默认获取最近24小时的变更
            if not start_time:
                start_time = datetime.utcnow() - timedelta(days=1)
                
            # 转换为RFC 3339格式
            time_str = start_time.isoformat("T") + "Z"
            
            results = service.files().list(
                q=f"modifiedTime > '{time_str}'",
                pageSize=100,
                fields="files(id, name, mimeType, modifiedTime)"
            ).execute()
            
            return results.get('files', [])
        except Exception as e:
            logger.error(f"获取变更失败: {str(e)}")
            return [] 
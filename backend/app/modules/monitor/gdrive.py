from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from typing import Optional, List, Dict, Any
import os
import json
from datetime import datetime, timezone
from loguru import logger
import pickle
import socket
import webbrowser
import http.server
import threading
import asyncio

class GoogleDriveClient:
    SCOPES = [
        'https://www.googleapis.com/auth/drive.readonly',
        'https://www.googleapis.com/auth/drive.activity.readonly'
    ]

    def __init__(self, client_id: str, client_secret: str, token_file: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_file = token_file
        self.creds: Optional[Credentials] = None
        self.drive_service = None
        self.activity_service = None
        self.last_check_time = None

    def load_rclone_token(self, rclone_config_path: str) -> bool:
        """从rclone配置文件加载token"""
        try:
            with open(rclone_config_path, 'r') as f:
                for line in f:
                    if line.startswith("token = "):
                        token_data = json.loads(line.split("=", 1)[1].strip())
                        self.creds = Credentials.from_authorized_user_info(token_data, self.SCOPES)
                        return True
            return False
        except Exception as e:
            logger.error(f"Error loading rclone token: {str(e)}")
            return False

    class AuthServer(http.server.HTTPServer):
        auth_code = None

    class AuthHandler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            """处理OAuth回调"""
            if "code=" in self.path:
                self.server.auth_code = self.path.split("code=")[1].split("&")[0]
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"Authorization successful! You can close this window.")
            else:
                self.send_response(400)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"Authorization failed!")

        def log_message(self, format: str, *args: Any) -> None:
            """禁用HTTP服务器日志"""
            pass

    async def authenticate(self, remote_auth: bool = False):
        """认证并获取Google Drive访问权限
        
        Args:
            remote_auth: 是否使用远程认证模式
        """
        # 尝试加载现有token
        if os.path.exists(self.token_file):
            try:
                with open(self.token_file, 'r') as token:
                    self.creds = Credentials.from_authorized_user_info(
                        json.load(token), self.SCOPES)
            except Exception as e:
                logger.error(f"Error loading token file: {str(e)}")

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                if remote_auth:
                    self.creds = await self._remote_auth()
                else:
                    self.creds = await self._local_auth()

            # 保存token
            with open(self.token_file, 'w') as token:
                token.write(self.creds.to_json())

        # 初始化服务
        self.drive_service = build('drive', 'v3', credentials=self.creds)
        self.activity_service = build('driveactivity', 'v2', credentials=self.creds)
        self.last_check_time = datetime.now(timezone.utc)
        logger.info("Successfully authenticated with Google Drive")

    async def _local_auth(self) -> Credentials:
        """本地浏览器认证流程"""
        flow = InstalledAppFlow.from_client_config(
            {
                "installed": {
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "redirect_uris": ["http://localhost:0"],
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token"
                }
            },
            self.SCOPES
        )
        return flow.run_local_server(port=0)

    async def _remote_auth(self) -> Credentials:
        """远程认证流程"""
        # 创建临时HTTP服务器
        server = self.AuthServer(('', 0), self.AuthHandler)
        port = server.server_address[1]
        
        flow = InstalledAppFlow.from_client_config(
            {
                "installed": {
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "redirect_uris": [f"http://localhost:{port}"],
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token"
                }
            },
            self.SCOPES
        )

        auth_url = flow.authorization_url()[0]
        print("\n请在有浏览器的设备上访问以下地址进行授权：")
        print(f"\n{auth_url}\n")

        # 启动服务器等待回调
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True
        server_thread.start()

        # 等待认证码
        while not server.auth_code:
            await asyncio.sleep(1)

        server.shutdown()
        server_thread.join()

        # 使用认证码获取凭证
        flow.fetch_token(code=server.auth_code)
        return flow.credentials

    async def get_changes(self, page_size: int = 100) -> List[Dict]:
        """使用Activity API获取文件变更"""
        try:
            if not self.last_check_time:
                return []

            # 构建查询请求
            request_body = {
                'pageSize': page_size,
                'filter': f'time >= "{self.last_check_time.isoformat()}Z"'
            }

            response = self.activity_service.activity().query(
                body=request_body).execute()
            
            changes = []
            for activity in response.get('activities', []):
                # 解析活动数据
                target = activity.get('targets', [{}])[0]
                action = activity.get('primaryActionDetail', {})
                
                if 'driveItem' in target:
                    item = target['driveItem']
                    change = {
                        'file_id': item.get('name', ''),  # 这是文件ID
                        'title': item.get('title', ''),
                        'time': activity.get('timestamp', ''),
                        'action': next(iter(action.keys()), 'unknown')
                    }
                    changes.append(change)

            self.last_check_time = datetime.now(timezone.utc)
            return changes

        except Exception as e:
            logger.error(f"Error getting changes from Activity API: {str(e)}")
            raise

    async def list_files(self, folder_id: str = 'root') -> List[Dict]:
        """列出指定文件夹中的所有文件"""
        try:
            results = []
            page_token = None
            
            while True:
                response = self.drive_service.files().list(
                    q=f"'{folder_id}' in parents",
                    spaces='drive',
                    fields='nextPageToken, files(id, name, mimeType, modifiedTime, size)',
                    pageToken=page_token
                ).execute()

                files = response.get('files', [])
                results.extend(files)
                
                page_token = response.get('nextPageToken')
                if not page_token:
                    break

            return results
            
        except Exception as e:
            logger.error(f"Error listing files from Google Drive: {str(e)}")
            raise 
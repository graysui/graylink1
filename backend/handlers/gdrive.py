from fastapi import APIRouter, HTTPException, Request
from utils.gdrive import GoogleDriveAPI
from utils.config import get_config
from typing import Dict, Optional
from fastapi.responses import HTMLResponse

router = APIRouter()

@router.get("/gdrive/auth-url")
async def get_auth_url() -> Dict[str, str]:
    """获取Google Drive授权URL"""
    try:
        config = get_config()
        gdrive = GoogleDriveAPI(
            client_id=config.monitor.google_drive.client_id,
            client_secret=config.monitor.google_drive.client_secret,
            token_file=config.monitor.google_drive.token_file
        )
        auth_url = gdrive.get_auth_url()
        return {"auth_url": auth_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/gdrive/authorize")
async def authorize_gdrive(code: str):
    """使用授权码完成授权"""
    try:
        config = get_config()
        gdrive = GoogleDriveAPI(
            client_id=config.monitor.google_drive.client_id,
            client_secret=config.monitor.google_drive.client_secret,
            token_file=config.monitor.google_drive.token_file
        )
        gdrive.authorize_with_code(code)
        return {"message": "授权成功"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/gdrive/watch")
async def setup_watch():
    """设置文件夹监控"""
    try:
        config = get_config()
        gdrive = GoogleDriveAPI(
            client_id=config.monitor.google_drive.client_id,
            client_secret=config.monitor.google_drive.client_secret,
            token_file=config.monitor.google_drive.token_file
        )
        
        # 使用固定的webhook地址
        webhook_url = f"{config.server.base_url}/api/webhook/gdrive"
        
        result = gdrive.setup_watch(
            folder_id=config.monitor.google_drive.watch_folder_id,
            notification_url=webhook_url
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/webhook/gdrive")
async def handle_gdrive_change(request: Request):
    """处理Google Drive变更通知"""
    try:
        config = get_config()
        if not config.monitor.google_drive.enabled:
            return {"status": "disabled"}

        # 获取变更详情
        gdrive = GoogleDriveAPI(
            client_id=config.monitor.google_drive.client_id,
            client_secret=config.monitor.google_drive.client_secret,
            token_file=config.monitor.google_drive.token_file
        )
        
        changes = await gdrive.get_changes(request)
        
        # 处理每个变更
        for change in changes:
            if change.get('file') and not change.get('removed'):
                # 获取文件路径
                file_path = change['file']['path']
                
                # 转换为本地路径
                local_path = None
                for gdrive_path, local_dir in config.monitor.google_drive.path_mapping.items():
                    if file_path.startswith(gdrive_path):
                        local_path = file_path.replace(gdrive_path, local_dir)
                        break
                
                if local_path:
                    # 创建软链接
                    await create_symlink(local_path)
        
        return {"status": "success"}
    except Exception as e:
        logger.error(f"处理Google Drive变更失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))

def map_to_local_path(drive_path: str, path_mapping: Dict[str, str]) -> Optional[str]:
    """将 Google Drive 路径映射到本地路径"""
    for drive_prefix, local_prefix in path_mapping.items():
        if drive_path.startswith(drive_prefix):
            return drive_path.replace(drive_prefix, local_prefix)
    return None

@router.post("/gdrive/check-activities")
async def check_activities():
    """检查文件活动"""
    try:
        config = get_config()
        if not config.monitor.google_drive.enabled:
            return {"status": "disabled"}

        gdrive = GoogleDriveAPI(
            client_id=config.monitor.google_drive.client_id,
            client_secret=config.monitor.google_drive.client_secret,
            token_file=config.monitor.google_drive.token_file
        )
        
        activities = gdrive.get_activities(
            folder_id=config.monitor.google_drive.watch_folder_id,
            time_filter=config.monitor.google_drive.check_interval
        )
        
        # 处理新文件活动
        processed = 0
        for activity in activities:
            if activity['action_type'] in ['create', 'edit', 'move']:
                drive_path = activity['file']['path']
                # 转换为本地路径
                local_path = map_to_local_path(
                    drive_path,
                    config.monitor.google_drive.path_mapping
                )
                if local_path:
                    # 创建软链接
                    from utils.symlink import create_symlink
                    await create_symlink(local_path)
                    processed += 1
        
        return {
            "status": "success", 
            "activities": len(activities),
            "processed": processed
        }
    except Exception as e:
        logger.error(f"检查Drive活动失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/oauth2callback")
async def oauth2callback(code: str):
    """处理 Google OAuth 回调"""
    try:
        config = get_config()
        gdrive = GoogleDriveAPI(
            client_id=config.monitor.google_drive.client_id,
            client_secret=config.monitor.google_drive.client_secret,
            token_file=config.monitor.google_drive.token_file
        )
        await gdrive.handle_oauth_callback(code)
        # 返回HTML页面，显示授权成功并关闭窗口
        return HTMLResponse(content="""
            <html>
                <body>
                    <h1>授权成功！</h1>
                    <p>请关闭此窗口并返回应用。</p>
                    <script>
                        setTimeout(function() {
                            window.close();
                        }, 3000);
                    </script>
                </body>
            </html>
        """)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/gdrive/start-auth")
async def start_device_auth() -> Dict[str, str]:
    """开始设备授权流程"""
    try:
        config = get_config()
        gdrive = GoogleDriveAPI(
            client_id=config.monitor.google_drive.client_id,
            client_secret=config.monitor.google_drive.client_secret,
            token_file=config.monitor.google_drive.token_file
        )
        
        device_code_info = gdrive.get_device_code()
        return {
            "user_code": device_code_info['user_code'],
            "verification_url": device_code_info['verification_url'],
            "device_code": device_code_info['device_code'],
            "expires_in": device_code_info['expires_in']
        }

@router.post("/gdrive/check-auth")
async def check_device_auth(device_code: str):
    """检查授权状态"""
    try:
        config = get_config()
        gdrive = GoogleDriveAPI(
            client_id=config.monitor.google_drive.client_id,
            client_secret=config.monitor.google_drive.client_secret,
            token_file=config.monitor.google_drive.token_file
        )
        
        token_data = gdrive.poll_token(device_code)
        if token_data:
            gdrive.save_token(token_data)
            return {"status": "success"}
        return {"status": "pending"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
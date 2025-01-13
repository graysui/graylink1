import aiohttp
from fastapi import HTTPException

async def test_emby_connection(host: str, api_key: str) -> bool:
    """测试 Emby 服务器连接"""
    try:
        headers = {
            'X-Emby-Token': api_key,
            'Accept': 'application/json'
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{host}/emby/System/Info", headers=headers) as response:
                if response.status == 200:
                    return True
                else:
                    raise HTTPException(
                        status_code=400, 
                        detail=f"连接失败: HTTP {response.status}"
                    )
    except aiohttp.ClientError as e:
        raise HTTPException(status_code=400, detail=f"连接失败: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
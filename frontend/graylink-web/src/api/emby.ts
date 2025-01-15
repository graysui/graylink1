import type { ApiResponse, EmbyStatus } from '@/types/api'
import { request } from '@/utils/request'

export const embyApi = {
  // 检查Emby服务器状态
  checkStatus(): Promise<ApiResponse<EmbyStatus>> {
    return request.get('/api/emby/status')
  },

  // 获取媒体库列表
  getLibraries(): Promise<ApiResponse<string[]>> {
    return request.get('/api/emby/libraries')
  },

  // 刷新指定路径的媒体库
  refreshByPaths(paths: string[]): Promise<ApiResponse<void>> {
    return request.post('/api/emby/refresh', { paths })
  },

  // 刷新根目录
  refreshRoot(): Promise<ApiResponse<void>> {
    return request.post('/api/emby/refresh/root')
  },

  // 测试Emby连接
  test(server: string, apiKey: string): Promise<ApiResponse<EmbyStatus>> {
    return request.post('/api/emby/test', { server, api_key: apiKey })
  }
}

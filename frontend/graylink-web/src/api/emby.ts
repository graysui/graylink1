import { api } from '@/utils/request'
import type { EmbyLibrary, EmbyStatus } from '@/types/emby'
import type { ApiResponse } from '@/types/response'

export const embyApi = {
  // 检查服务器状态
  checkStatus() {
    return api.get<ApiResponse<EmbyStatus>>('/emby/status')
  },

  // 获取媒体库列表
  getLibraries() {
    return api.get<ApiResponse<EmbyLibrary[]>>('/emby/libraries')
  },

  // 按路径刷新媒体库
  refreshByPaths(paths: string[]) {
    return api.post<ApiResponse<void>>('/emby/refresh', { paths })
  },

  // 刷新整个媒体库
  refreshRoot() {
    return api.post<ApiResponse<void>>('/emby/refresh/root')
  },

  // 测试连接
  test() {
    return api.post<ApiResponse<void>>('/emby/test')
  },

  // 刷新媒体库
  refreshLibrary() {
    return api.post<ApiResponse<void>>('/emby/refresh')
  }
}

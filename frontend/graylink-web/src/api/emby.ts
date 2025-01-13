import request from '@/utils/request'
import type { EmbyLibrary, EmbyStatus } from '@/types/api'

export const embyApi = {
  // 检查服务器状态
  checkStatus() {
    return request.get<EmbyStatus>('/emby/status')
  },

  // 获取媒体库列表
  getLibraries() {
    return request.get<EmbyLibrary[]>('/emby/libraries')
  },

  // 按路径刷新媒体库
  refreshByPaths(paths: string[]) {
    return request.post('/emby/refresh', { paths })
  },

  // 刷新整个媒体库
  refreshRoot() {
    return request.post('/emby/refresh/root')
  },

  // 测试连接
  test() {
    return request.post('/emby/test')
  },

  // 刷新媒体库
  refreshLibrary() {
    return request.post('/emby/refresh')
  }
} 
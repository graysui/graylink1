import request from '@/utils/request'
import type { FileInfo, DatabaseStats } from '@/types/api'

export const fileApi = {
  getSnapshot: (path?: string) => request.get<FileInfo[]>('/files/snapshot', path ? { params: { path } } : undefined),
  getStats: () => request.get<DatabaseStats>('/files/stats'),
  cleanup: () => request.post('/files/cleanup'),
  delete: (paths: string[]) => request.post('/files/delete', { paths }),
  move: (paths: string[], target: string) => request.post('/files/move', { paths, target }),
  copy: (paths: string[], target: string) => request.post('/files/copy', { paths, target }),
  // 获取目录列表
  listDirectory(path: string) {
    return request.get<FileInfo[]>('/file/list', {
      params: { path }
    })
  }
} 
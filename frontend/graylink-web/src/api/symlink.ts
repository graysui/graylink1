import request from '@/utils/request'
import type { SymlinkResult } from '@/types/api'

export const symlinkApi = {
  // 创建软链接
  create(relativePath: string) {
    return request.post<SymlinkResult>('/symlink/create', { relative_path: relativePath })
  },

  // 删除软链接
  remove(relativePath: string) {
    return request.post<SymlinkResult>('/symlink/remove', { relative_path: relativePath })
  },

  // 验证软链接
  verify() {
    return request.get('/symlink/verify')
  },

  // 重建所有软链接
  rebuild() {
    return request.post('/symlink/rebuild')
  },

  // 清理所有软链接
  clear() {
    return request.post<SymlinkResult>('/symlink/clear')
  }
} 
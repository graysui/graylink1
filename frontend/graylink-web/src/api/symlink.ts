import { request } from '@/utils/request'
import type { ApiResponse, SymlinkState } from '@/types/api'

export const symlinkApi = {
  verify(): Promise<ApiResponse<SymlinkState>> {
    return request.get('/api/symlink/verify')
  },

  create(data: { source: string; target: string }): Promise<ApiResponse<void>> {
    return request.post('/api/symlink', data)
  },

  remove(id: string): Promise<ApiResponse<void>> {
    return request.delete(`/api/symlink/${id}`)
  },

  clear(): Promise<ApiResponse<void>> {
    return request.delete('/api/symlink')
  },

  rebuild(): Promise<ApiResponse<void>> {
    return request.post('/api/symlink/rebuild')
  }
}

import { api } from '@/utils/request'
import type { SymlinkState } from '@/types/symlink'

export const symlinkApi = {
  verify: () => api.get<SymlinkState>('/symlink/verify'),
  create: (data: { source: string; target: string }) => api.post('/symlink', data),
  remove: (id: string) => api.delete(`/symlink/${id}`),
  clear: () => api.delete('/symlink'),
  rebuild: () => api.post('/symlink/rebuild')
}

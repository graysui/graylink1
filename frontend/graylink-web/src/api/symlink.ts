import { api } from '@/utils/request'
import type { SymlinkState } from '@/types/symlink'

export const symlinkApi = {
  verify: () => api.get<SymlinkState>('/symlinks/verify'),
  create: (data: { source: string; target: string }) => api.post('/symlinks', data),
  remove: (id: string) => api.delete(`/symlinks/${id}`),
  clear: () => api.delete('/symlinks'),
  rebuild: () => api.post('/symlinks/rebuild')
}

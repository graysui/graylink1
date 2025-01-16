import { request } from '@/utils/request'
import type { ApiResponse, SystemSettings } from '@/types/api'

export const settingApi = {
  getSettings(): Promise<ApiResponse<SystemSettings>> {
    return request.get('/api/setting')
  },

  updateSettings(data: SystemSettings): Promise<ApiResponse<void>> {
    return request.put('/api/setting', data)
  },

  resetSettings(): Promise<ApiResponse<void>> {
    return request.post('/api/setting/reset')
  }
}

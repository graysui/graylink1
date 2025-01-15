import { request } from '@/utils/request'
import type { ApiResponse, SystemSettings } from '@/types/api'

export const settingApi = {
  getSettings(): Promise<ApiResponse<SystemSettings>> {
    return request.get('/api/settings')
  },

  updateSettings(data: SystemSettings): Promise<ApiResponse<void>> {
    return request.post('/api/settings', data)
  },

  resetSettings(): Promise<ApiResponse<void>> {
    return request.post('/api/settings/reset')
  }
}

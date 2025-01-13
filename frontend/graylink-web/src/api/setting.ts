import request from '@/utils/request'
import type { ApiResponse, SystemSettings } from '@/types/api'

export interface EmbyConnectionTest {
  host: string
  api_key: string
}

export const settingApi = {
  getSettings() {
    return request.get<ApiResponse<SystemSettings>>('/settings')
  },

  updateSettings(settings: SystemSettings) {
    return request.post<ApiResponse<void>>('/settings', settings)
  },

  testEmbyConnection(params: EmbyConnectionTest) {
    return request.post<ApiResponse<void>>('/settings/test-emby', params)
  },

  updatePassword(data: { new_password: string }) {
    return request.post<ApiResponse<void>>('/settings/password', data)
  }
} 
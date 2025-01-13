import request from '@/utils/request'
import type { SystemSettings } from '@/types/api'

export interface EmbyConnectionTest {
  host: string
  api_key: string
}

export const settingApi = {
  // 获取系统设置
  getSettings() {
    return request.get<SystemSettings>('/settings')
  },

  // 保存系统设置
  saveSettings(settings: SystemSettings) {
    return request.post<void>('/settings', settings)
  },

  // 测试 Emby 连接
  testEmbyConnection(params: EmbyConnectionTest) {
    return request.post<void>('/settings/test-emby', params)
  },

  // 重置系统设置
  resetSettings() {
    return request.post<void>('/settings/reset')
  }
} 
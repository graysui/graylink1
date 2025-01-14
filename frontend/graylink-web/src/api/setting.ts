import { api } from '@/utils/request'
import type { SystemSettings } from '@/types/settings'

export const settingApi = {
  getSettings: () => api.get<SystemSettings>('/settings'),
  updateSettings: (settings: Partial<SystemSettings>) => api.post('/settings', settings),
  resetSettings: () => api.post('/settings/reset')
}

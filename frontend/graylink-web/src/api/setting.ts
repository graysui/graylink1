import { request } from '@/utils/request'

export interface SettingForm {
  monitorPath: string
  embyServer: string
  embyApiKey: string
  gdriveClientId: string
  gdriveClientSecret: string
}

export const settingApi = {
  updateSettings(data: SettingForm) {
    return request.post('/api/setting', data)
  },

  resetSettings() {
    return request.post('/api/setting/reset')
  }
}

import { defineStore } from 'pinia'
import { ref } from 'vue'
import { request } from '@/utils/request'
import type { SystemSettings, ApiResponse } from '@/types/api'

interface EmbySettings {
  server: string
  api_key: string
}

export const useSettingStore = defineStore('setting', () => {
  const settings = ref<SystemSettings>()

  const getSettings = async () => {
    const response = await request.get<ApiResponse<SystemSettings>>('/api/setting')
    settings.value = response.data.data
    return response.data.data
  }

  const saveSettings = async (settings: SystemSettings) => {
    await request.post<ApiResponse<void>>('/api/setting', settings)
  }

  const testEmbyConnection = async (emby: EmbySettings) => {
    await request.post<ApiResponse<void>>('/api/emby/test', emby)
  }

  const updatePassword = async (password: string, confirmPassword: string) => {
    await request.post<ApiResponse<void>>('/api/user/password', {
      password,
      confirm_password: confirmPassword
    })
  }

  return {
    settings,
    getSettings,
    saveSettings,
    testEmbyConnection,
    updatePassword
  }
})

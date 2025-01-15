import { defineStore } from 'pinia'
import { ref } from 'vue'
import { request } from '@/utils/request'
import type { SystemSettings, EmbySettings } from '@/types/settings'

export const useSettingStore = defineStore('setting', () => {
  const settings = ref<SystemSettings>()

  const getSettings = async () => {
    const { data } = await request.get<SystemSettings>('/api/setting')
    settings.value = data
    return data
  }

  const saveSettings = async (settings: SystemSettings) => {
    await request.post('/api/setting', settings)
  }

  const testEmbyConnection = async (emby: EmbySettings) => {
    await request.post('/api/emby/test', emby)
  }

  const updatePassword = async (password: string, confirmPassword: string) => {
    await request.post('/api/user/password', {
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

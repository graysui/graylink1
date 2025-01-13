import { defineStore } from 'pinia'
import { ref } from 'vue'
import { settingApi } from '@/api/setting'
import type { SystemSettings } from '@/types/api'
import type { EmbyConnectionTest } from '@/api/setting'

export const useSettingStore = defineStore('setting', () => {
  // 状态
  const settings = ref<SystemSettings>({
    monitor: {
      interval: 300,
      batch_size: 100,
      max_retries: 3
    },
    symlink: {
      source_dir: '/mnt/media/nastool',
      target_dir: '/mnt/nastool-nfo',
      preserve_structure: true,
      backup_on_conflict: true,
      conflict_strategy: 'skip'
    },
    emby: {
      host: 'http://emby:8096',
      api_key: '',
      auto_refresh: true,
      refresh_delay: 10,
      path_mapping: {}
    },
    security: {
      max_login_attempts: 5,
      session_timeout: 3600,
      password_policy: {
        min_length: 8,
        require_special: true,
        require_numbers: true
      }
    }
  })
  const loading = ref(false)

  // actions
  const getSettings = async () => {
    try {
      loading.value = true
      const result = await settingApi.getSettings()
      settings.value = result
      return result
    } catch (error) {
      console.error('获取设置失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  const saveSettings = async (newSettings: SystemSettings) => {
    try {
      loading.value = true
      await settingApi.saveSettings(newSettings)
      settings.value = newSettings
    } catch (error) {
      console.error('保存设置失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  const testEmbyConnection = async (params: EmbyConnectionTest) => {
    try {
      loading.value = true
      await settingApi.testEmbyConnection(params)
    } catch (error) {
      console.error('测试Emby连接失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  const resetSettings = async () => {
    try {
      loading.value = true
      await settingApi.resetSettings()
      await getSettings() // 重新加载默认设置
    } catch (error) {
      console.error('重置设置失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  return {
    settings,
    loading,
    getSettings,
    saveSettings,
    testEmbyConnection,
    resetSettings
  }
}) 
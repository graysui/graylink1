import { defineStore } from 'pinia'
import { ref } from 'vue'
import { settingApi } from '@/api/setting'
import type { SystemSettings } from '@/types/api'

export const useSettingStore = defineStore('setting', () => {
  const settings = ref<SystemSettings>({
    monitor: {
      interval: 5000,
      batch_size: 100,
      max_retries: 3,
      google_drive: {
        enabled: false,
        client_id: '',
        client_secret: '',
        token_file: '',
        watch_folder_id: '',
        check_interval: '5m',
        path_mapping: {}
      }
    },
    symlink: {
      source_dir: '',
      target_dir: '',
      preserve_structure: true,
      backup_on_conflict: true,
      conflict_strategy: 'skip'
    },
    emby: {
      host: '',
      api_key: '',
      auto_refresh: false,
      refresh_delay: 5000,
      path_mapping: {}
    }
  })

  const loading = ref(false)

  const getSettings = async () => {
    loading.value = true
    try {
      const { data } = await settingApi.getSettings()
      settings.value = data
    } finally {
      loading.value = false
    }
  }

  const saveSettings = async (newSettings: SystemSettings) => {
    loading.value = true
    try {
      await settingApi.updateSettings(newSettings)
      settings.value = newSettings
    } finally {
      loading.value = false
    }
  }

  return {
    settings,
    loading,
    getSettings,
    saveSettings
  }
}) 
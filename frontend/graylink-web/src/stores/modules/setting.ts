import { defineStore } from 'pinia'
import type { SystemSettings } from '@/types/settings'
import { api } from '@/api'
import type { ApiResponse } from '@/types/api'

interface SettingState {
  settings: SystemSettings
  loading: boolean
}

const testEmbyConnection = async (config: SystemSettings['emby']) => {
  try {
    await api.post('/emby/test', config)
    return true
  } catch (error) {
    throw new Error('连接失败')
  }
}

export const useSettingStore = defineStore('setting', {
  state: (): SettingState => ({
    settings: {
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
          check_interval: '1h',
          refresh_token: '',
          path_mapping: {},
        },
      },
      symlink: {
        source_dir: '',
        target_dir: '',
        preserve_structure: true,
        backup_on_conflict: true,
        conflict_strategy: 'rename',
        auto_rebuild: false,
        rebuild_interval: 3600,
        path_mapping: {},
      },
      emby: {
        host: '',
        api_key: '',
        auto_refresh: false,
        refresh_delay: 5000,
        server_url: '',
        library_path: '',
        path_mapping: {},
      },
      security: {
        jwt_secret: '',
        token_expire: 7200,
        max_login_attempts: 5,
        session_timeout: 3600,
        password_policy: {
          min_length: 8,
          require_special: true,
          require_numbers: true,
        },
      },
      account: {
        username: '',
        email: '',
        password: '',
        confirm_password: '',
        allow_register: true,
        default_role: 'user',
      },
    },
    loading: false,
  }),

  actions: {
    async getSettings() {
      this.loading = true
      try {
        const response = await api.get<ApiResponse<SystemSettings>>('/settings')
        this.settings = response.data
      } finally {
        this.loading = false
      }
    },

    async saveSettings(settings: SystemSettings) {
      this.loading = true
      try {
        await api.post('/settings', settings)
        this.settings = settings
      } finally {
        this.loading = false
      }
    },

    async updatePassword(oldPassword: string, newPassword: string) {
      this.loading = true
      try {
        await api.post('/settings/password', {
          old_password: oldPassword,
          new_password: newPassword,
        })
      } finally {
        this.loading = false
      }
    },

    testEmbyConnection,
  },
})

import type { Ref } from 'vue'
import type { SystemSettings } from '@/types/api'

export interface UserInfo {
  username: string
  role: string
  created_at: string
  updated_at: string
}

export interface UserState {
  token: Ref<string | null>
  username: Ref<string>
  userInfo: Ref<UserInfo | null>
  hasToken: boolean
  login: (form: LoginForm) => Promise<void>
  logout: () => void
}

export interface LoginForm {
  username: string
  password: string
}

export interface MonitorState {
  status: Ref<{
    running: boolean
    lastCheck: string | null
    stats: {
      totalFiles: number
      processedFiles: number
      errorCount: number
      lastError?: string
    }
  }>
  loading: Ref<boolean>
  startMonitor: () => Promise<void>
  stopMonitor: () => Promise<void>
}

export interface SettingStore {
  settings: Ref<SystemSettings>
  loading: Ref<boolean>
  saveSettings: (settings: SystemSettings) => Promise<void>
}

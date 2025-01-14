import type { EmbyLibrary, EmbyStatus } from './emby'

export interface FileItem {
  name: string
  path: string
  type: 'file' | 'directory'
  size: number
  modTime: string
}

export interface SystemSettings {
  monitor: {
    interval: number
    batch_size: number
    max_retries: number
    google_drive: {
      enabled: boolean
      client_id: string
      client_secret: string
      token_file: string
      refresh_token?: string
      watch_folder_id: string
      check_interval: string
      path_mapping: Record<string, string>
    }
  }
  symlink: {
    source_dir: string
    target_dir: string
    auto_rebuild: boolean
    rebuild_interval: number
    preserve_structure: boolean
    backup_on_conflict: boolean
    conflict_strategy: 'skip' | 'overwrite' | 'rename'
  }
  emby: {
    server_url: string
    library_path: string
    api_key: string
    auto_refresh: boolean
    refresh_delay: number
    path_mapping: Record<string, string>
  }
  security: {
    jwt_secret: string
    token_expire: number
    max_login_attempts: number
  }
  account: {
    allow_register: boolean
    default_role: string
    username?: string
    password?: string
    confirm_password?: string
  }
}

export interface VerifyResult {
  valid: boolean
  errors: string[]
  warnings: string[]
}

export interface ApiResponse<T = any> {
  code: number
  data: T
  message: string
}

export interface SettingState {
  settings: SystemSettings
}

export interface EmbyState {
  libraries: EmbyLibrary[]
  status: EmbyStatus
  refreshProgress: Record<string, number>
}

export interface FileState {
  currentPath: string
  files: FileItem[]
  sorting: {
    prop: string
    order: 'ascending' | 'descending'
  }
}

export interface SymlinkState {
  verifyResult: VerifyResult
  progress: {
    current: number
    total: number
    message?: string
  }
}

export interface SettingStore {
  getSettings(): Promise<void>
  saveSettings(settings: SystemSettings): Promise<void>
  updatePassword(oldPassword: string, newPassword: string): Promise<void>
  testEmbyConnection(config: SystemSettings['emby']): Promise<void>
}

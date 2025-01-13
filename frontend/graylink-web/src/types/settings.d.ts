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
      watch_folder_id: string
      check_interval: string
      refresh_token: string
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
    conflict_strategy: 'skip' | 'rename' | 'overwrite'
    path_mapping: Record<string, string>
  }
  emby: {
    host: string
    api_key: string
    auto_refresh: boolean
    refresh_delay: number
    server_url: string
    library_path: string
    path_mapping: Record<string, string>
  }
  security: {
    jwt_secret: string
    token_expire: number
    max_login_attempts: number
    session_timeout: number
    password_policy: {
      min_length: number
      require_special: boolean
      require_numbers: boolean
    }
  }
  account: {
    username: string
    email: string
    password: string
    confirm_password: string
    allow_register: boolean
    default_role: string
  }
}

export interface EmbyLibrary {
  id: string
  name: string
  path: string
  type: string
  lastScan?: string
  refreshing?: boolean
}

export interface EmbyStatus {
  connected: boolean
  version: string
  lastUpdate?: string
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

export interface GoogleDriveSettings {
  enabled: boolean
  client_id: string
  client_secret: string
  token_file: string
  watch_folder_id: string
  check_interval: string
  path_mapping: Record<string, string>
  refresh_token: string
}

export interface MonitorSettings {
  interval: number
  batch_size: number
  max_retries: number
  google_drive: GoogleDriveSettings
}

export interface SymlinkSettings {
  source_dir: string
  target_dir: string
  auto_rebuild: boolean
  rebuild_interval: number
  conflict_strategy: string
  preserve_structure: boolean
  backup_on_conflict: boolean
  path_mapping: Record<string, string>
}

export interface EmbySettings {
  host: string
  api_key: string
  auto_refresh: boolean
  refresh_delay: number
  path_mapping: Record<string, string>
  server_url: string
  library_path: string
}

export interface PasswordPolicy {
  min_length: number
  require_uppercase: boolean
  require_lowercase: boolean
  require_numbers: boolean
  require_special: boolean
}

export interface SecuritySettings {
  jwt_secret: string
  token_expire: number
  max_login_attempts: number
  session_timeout: number
  password_policy: PasswordPolicy
}

export interface AccountSettings {
  allow_register: boolean
  default_role: string
  username: string
  password: string
  confirm_password: string
}

export interface SystemSettings {
  monitor: MonitorSettings
  symlink: SymlinkSettings
  emby: EmbySettings
  security: SecuritySettings
  account: AccountSettings
}

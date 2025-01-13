// 基础响应类型
export interface ApiResponse<T> {
  data: T
  status: string
  message?: string
}

export interface PaginationData<T> {
  items: T[]
  total: number
  page: number
  pageSize: number
}

export interface PaginatedResponse<T> extends Omit<ApiResponse<any>, 'data'> {
  data: PaginationData<T>
}

export interface ErrorResponse {
  error: string
  message: string
  status: number
}

// FileRecord 类型定义
export interface FileRecord {
  id: string
  name: string
  path: string
  size: number
  type: string
  modified_time: string
  is_directory: boolean
  parent_id?: string
  children?: FileRecord[]
  meta?: Record<string, any>
}

// DatabaseStats 类型定义
export interface DatabaseStats {
  total_size: number
  file_count: number
  database: {
    total_size: number
    index_size: number
    table_count: number
  }
  performance: {
    slow_queries: Array<{
      query: string
      duration: number
      timestamp: string
    }>
    query_stats: {
      total: number
      slow: number
      average_duration: number
    }
  }
}

// Settings 相关类型定义
export interface BasicSettings {
  scan_interval: number
  batch_size: number
  max_retries: number
  auto_cleanup: boolean
  cleanup_threshold: number
}

export interface PathConfig {
  id: string
  path: string
  type: 'source' | 'target'
  enabled: boolean
  priority: number
  filters?: string[]
}

export interface ScheduleSettings {
  enabled: boolean
  cron: string
  tasks: Array<{
    type: 'scan' | 'cleanup' | 'optimize'
    enabled: boolean
    params?: Record<string, any>
  }>
}

export interface Settings {
  basic: BasicSettings
  paths: PathConfig[]
  schedule: ScheduleSettings
}

// SymlinkResult 类型定义
export interface SymlinkResult {
  success: boolean
  source: string
  target: string
  error?: string
  created_time?: string
  status: 'valid' | 'broken' | 'missing'
}

// 导出其他必要的类型
export interface FileInfo {
  id: string
  name: string
  path: string
  size: number
  type: string
  modified_time: string
  is_directory: boolean
  preview_url?: string
  download_url?: string
  meta?: Record<string, any>
}

export interface MonitorStatus {
  status: 'running' | 'stopped'
  last_check: string | null
  interval: number
  stats: {
    total_files: number
    processed_files: number
    pending_files: number
    error_count: number
    last_error?: string
    scan_speed?: number
    estimated_time?: number
  }
}

export interface EmbyLibrary {
  id: string
  name: string
  path: string
  type: string
  itemCount: number
  lastUpdate?: string
}

// 添加 UserInfo 类型定义
export interface UserInfo {
  id: number
  username: string
  email: string
  avatar?: string
  roles: string[]
  permissions: string[]
  settings?: Record<string, any>
  created_at: string
  updated_at: string
}

// 添加 SystemSettings 类型定义
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
      path_mapping: Record<string, string>
    }
  }
  symlink: {
    source_dir: string
    target_dir: string
    preserve_structure: boolean
    backup_on_conflict: boolean
    conflict_strategy: string
  }
  emby: {
    host: string
    api_key: string
    auto_refresh: boolean
    refresh_delay: number
    path_mapping: Record<string, string>
  }
  security: {
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
  }
}

export interface VerifyResult {
  broken_links: string[]
  invalid_targets: string[]
  timestamp?: string
  stats?: {
    total: number
    broken: number
    invalid: number
  }
}

// 修改 SymlinkStore 的类型
export interface SymlinkStore {
  verifyResult: VerifyResult | null
  loading: boolean
  verifySymlinks: () => Promise<void>
  createSymlink: (path: string) => Promise<void>
  removeSymlink: (path: string) => Promise<void>
  rebuildSymlinks: () => Promise<void>
  clearSymlinks: () => Promise<void>
}

export interface EmbyStatus {
  serverStatus: 'connected' | 'disconnected'
  apiStatus: boolean
  version?: string
  lastCheck?: string
}

export interface RcloneConfig {
  config_file: string
  remote_name: string
  mount_point: string
  mount_options: Record<string, string>
  auto_mount: boolean
}

export interface GoogleDriveConfig {
  client_id: string
  client_secret: string
  token_file: string
  refresh_token?: string
  watch_folder_id: string
  enabled: boolean
  check_interval: string
  path_mapping: Record<string, string>
}

export interface MonitorConfig {
  interval: number
  batch_size: number
  max_retries: number
  google_drive: GoogleDriveConfig
  rclone: RcloneConfig
}

export interface UserInfo {
  username: string
  email: string
}

export interface ChangePasswordParams {
  new_password: string
}

// 添加 Google Drive 相关类型定义
export interface DriveActivity {
  action_type: 'create' | 'edit' | 'move'
  time: string
  file: {
    id: string
    title: string
    path: string
    mime_type: string
  }
}

export interface DriveMonitorStatus {
  enabled: boolean
  check_interval: string
  last_check: string | null
  folder_name: string
  stats: {
    total_activities: number
    processed_files: number
    error_count: number
  }
}

export interface ActivityResult {
  activities: number
  processed: number
} 
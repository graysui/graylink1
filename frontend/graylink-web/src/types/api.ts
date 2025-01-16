// 基础响应类型
export interface ApiResponse<T> {
  code: number
  message: string
  data: T
}

// 错误响应类型
export interface ErrorResponse {
  error: string
  message: string
  status: number
}

// 分页数据类型
export interface PaginationData<T> {
  items: T[]
  total: number
  page: number
  page_size: number
}

// 分页响应类型
export interface PaginatedResponse<T> extends Omit<ApiResponse<any>, 'data'> {
  data: PaginationData<T>
}

// 扩展 axios 类型
declare module 'axios' {
  export interface AxiosResponse<T = any> {
    data: ApiResponse<T>
    status: number
    statusText: string
    headers: Record<string, string>
    config: AxiosRequestConfig
  }
}

// 文件记录类型
export interface FileRecord {
  name: string
  path: string
  type: 'file' | 'directory'
  size: number
  modified: string
  extension?: string
}

// 日志数据类型
export interface LogData {
  timestamp: number
  time: string
  level: 'info' | 'warning' | 'error'
  message: string
}

// 监控状态类型
export interface MonitorStatus {
  is_running: boolean
  last_check: string | null
  total_files: number
  monitored_paths: string[]
  interval?: number
  stats?: {
    total_files: number
    processed_files: number
    pending_files: number
    error_count: number
    last_error?: string
    scan_speed?: number
    estimated_time?: number
  }
  logs?: LogData[]
}

// Emby类型定义
export interface EmbyLibrary {
  id: string
  name: string
  path: string
  type: string
  itemCount?: number
  lastUpdate?: string
  refreshing?: boolean
}

export interface EmbyStatus {
  connected: boolean
  version: string | null
  server_name: string | null
  serverStatus?: 'connected' | 'disconnected'
  apiStatus?: boolean
  lastCheck?: string
  lastUpdate?: string
}

export interface EmbyState {
  status: EmbyStatus
  libraries: EmbyLibrary[]
  refreshProgress: Record<string, number>
}

// Google Drive活动类型
export interface DriveActivity {
  id?: string
  time: string
  type?: string
  action?: string
  actorEmail?: string
  targetName?: string
  targetId?: string
  file_name?: string
  file_id?: string
}

export interface ActivityResult {
  activities: DriveActivity[]
  next_page_token?: string
  processed?: number
  items?: DriveActivity[]
}

// 软链接类型定义
export interface Symlink {
  id: string
  source: string
  target: string
  status: 'valid' | 'invalid' | 'missing'
  lastCheck?: string
}

export interface SymlinkState {
  total: number
  valid: number
  invalid: number
  missing: number
  symlinks?: {
    value: Symlink[]
  }
  verifying?: boolean
  verifyResult?: {
    valid: number
    invalid: number
    missing: number
  }
  loading?: boolean
}

// 系统设置类型
export interface SystemSettings {
  emby_url: string
  emby_api_key: string
  monitor_interval: number
  monitor_paths: string[]
  monitor_extensions: string[]
  monitor_exclude_paths: string[]
  monitor_exclude_extensions: string[]
  monitor_auto_start: boolean
}

// 用户相关类型
export interface LoginForm {
  username: string
  password: string
}

export interface UserProfile {
  username: string
  created_at: string
  updated_at: string
}

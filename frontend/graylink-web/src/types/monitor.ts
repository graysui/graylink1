// 首先定义监控相关的类型
export interface LogData {
  timestamp: string
  level: string
  message: string
  time?: string  // 用于显示的格式化时间
}

export interface MonitorState {
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
  logs: LogData[]
  loading: boolean
}

export interface DriveActivity {
  id: string
  time: string
  type: string
  actorEmail?: string
  targetName: string
  targetId: string
}

export interface ActivityResult {
  activities: number
  processed: number
  items?: DriveActivity[]
}

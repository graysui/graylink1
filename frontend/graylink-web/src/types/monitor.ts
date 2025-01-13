// 首先定义监控相关的类型
export interface MonitorLog {
  timestamp: number
  level: 'info' | 'warning' | 'error'
  message: string
}

export interface MonitorStats {
  total: number
  success: number
  error: number
  warning: number
  lastUpdate?: string
}

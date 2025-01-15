import { request } from '@/utils/request'
import type { ApiResponse, MonitorStatus } from '@/types/api'

export interface MonitorLog {
  time: string
  level: 'error' | 'warning' | 'info'
  message: string
}

export interface MonitorStats {
  total_checks: number
  total_changes: number
  last_check_duration: number
}

export const monitorApi = {
  getStatus(): Promise<ApiResponse<MonitorStatus>> {
    return request.get('/api/monitor/status')
  },

  start(): Promise<ApiResponse<void>> {
    return request.post('/api/monitor/start')
  },

  stop(): Promise<ApiResponse<void>> {
    return request.post('/api/monitor/stop')
  },

  getLogs(limit: number = 100): Promise<ApiResponse<MonitorLog[]>> {
    return request.get('/api/monitor/logs', { params: { limit } })
  },

  clearLogs(): Promise<ApiResponse<void>> {
    return request.post('/api/monitor/logs/clear')
  },

  getStats(): Promise<ApiResponse<MonitorStats>> {
    return request.get('/api/monitor/stats')
  }
}

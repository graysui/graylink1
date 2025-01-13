import request from '@/utils/request'
import type { ApiResponse, MonitorStatus, ActivityResult } from '@/types/api'

export const monitorApi = {
  getStatus() {
    return request.get<ApiResponse<MonitorStatus>>('/monitor/status')
  },

  start() {
    return request.post<ApiResponse<void>>('/monitor/start')
  },

  stop() {
    return request.post<ApiResponse<void>>('/monitor/stop')
  },

  getLogs(params: { limit: number }) {
    return request.get<ApiResponse<string[]>>('/monitor/logs', { params })
  },

  clearLogs() {
    return request.post<ApiResponse<void>>('/monitor/logs/clear')
  },

  checkActivities() {
    return request.get<ApiResponse<ActivityResult>>('/monitor/check-activities')
  }
} 
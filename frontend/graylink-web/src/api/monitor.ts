import { api } from '@/utils/request'
import type { MonitorState } from '@/types/monitor'
import type { ApiResponse } from '@/types/response'

export const monitorApi = {
  getStatus: () => api.get<ApiResponse<MonitorState>>('/monitor/status'),
  start: () => api.post('/monitor/start'),
  stop: () => api.post('/monitor/stop'),
  getLogs: (params?: { limit: number }) => api.get('/monitor/logs', { params }),
  clearLogs: () => api.post('/monitor/logs/clear'),
  getStats: () => api.get('/monitor/stats')
}

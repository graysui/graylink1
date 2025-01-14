import { api } from '@/utils/request'
import type { MonitorState } from '@/types/monitor'

export const monitorApi = {
  getStatus: () => api.get<MonitorState>('/monitor/status'),
  start: () => api.post('/monitor/start'),
  stop: () => api.post('/monitor/stop'),
  getLogs: (params?: any) => api.get('/monitor/logs', { params }),
  clearLogs: () => api.post('/monitor/logs/clear'),
  getStats: () => api.get('/monitor/stats')
}

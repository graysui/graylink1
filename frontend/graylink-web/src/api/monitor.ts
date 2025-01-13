import request from '@/utils/request'

export interface MonitorStatus {
  running: boolean
  interval: number
  last_scan: string | null
  stats: {
    new_files: number
    processed_files: number
  }
}

export const monitorApi = {
  // 获取监控状态
  getStatus() {
    return request.get<MonitorStatus>('/monitor/status')
  },

  // 启动监控
  start() {
    return request.post('/monitor/start')
  },

  // 停止监控
  stop() {
    return request.post('/monitor/stop')
  }
} 
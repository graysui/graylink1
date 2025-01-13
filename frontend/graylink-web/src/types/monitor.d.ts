export interface LogData {
  timestamp: number
  time: string
  level: 'info' | 'warning' | 'error'
  message: string
}

// 在monitor/index.vue中使用正确的类型
const logs = ref<LogData[]>([])

import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { MonitorState } from '../types'

export const useMonitorStore = defineStore('monitor', () => {
  const status = ref<MonitorState['status']['value']>({
    running: false,
    lastCheck: null,
    stats: {
      totalFiles: 0,
      processedFiles: 0,
      errorCount: 0
    }
  })

  return {
    status
  }
}) 
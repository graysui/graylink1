import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { MonitorStatus, ApiResponse } from '@/types/api'
import { request } from '@/utils/request'

export const useMonitorStore = defineStore('monitor', () => {
  const status = ref<MonitorStatus>({
    is_running: false,
    last_check: null,
    total_files: 0,
    monitored_paths: []
  })

  const loading = ref(false)

  async function getStatus() {
    loading.value = true
    try {
      const response = await request.get<ApiResponse<MonitorStatus>>('/api/monitor/status')
      status.value = response.data.data
    } finally {
      loading.value = false
    }
  }

  async function startMonitor() {
    loading.value = true
    try {
      await request.post<ApiResponse<void>>('/api/monitor/start')
      await getStatus()
    } finally {
      loading.value = false
    }
  }

  async function stopMonitor() {
    loading.value = true
    try {
      await request.post<ApiResponse<void>>('/api/monitor/stop')
      await getStatus()
    } finally {
      loading.value = false
    }
  }

  return {
    status,
    loading,
    getStatus,
    startMonitor,
    stopMonitor
  }
})

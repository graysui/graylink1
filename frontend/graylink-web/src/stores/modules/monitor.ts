import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { monitorApi } from '@/api'
import type { MonitorStatus } from '@/types/api'

export const useMonitorStore = defineStore('monitor', () => {
  // 状态
  const status = ref<MonitorStatus>({
    status: 'stopped',
    last_check: null,
    stats: {
      total_files: 0,
      processed_files: 0,
      pending_files: 0,
      error_count: 0
    }
  })
  const loading = ref(false)
  const updateInterval = ref<number | null>(null)

  // 计算属性
  const isRunning = computed(() => status.value.status === 'running')
  const progress = computed(() => {
    const { processed_files, total_files } = status.value.stats
    if (total_files === 0) return 0
    return Math.round((processed_files / total_files) * 100)
  })

  // 开始自动更新
  function startAutoUpdate(interval = 5000) {
    stopAutoUpdate()
    updateInterval.value = window.setInterval(() => {
      if (isRunning.value) {
        getStatus()
      }
    }, interval)
  }

  // 停止自动更新
  function stopAutoUpdate() {
    if (updateInterval.value) {
      clearInterval(updateInterval.value)
      updateInterval.value = null
    }
  }

  // actions
  async function getStatus() {
    if (loading.value) return
    try {
      loading.value = true
      const result = await monitorApi.getStatus()
      status.value = result
    } catch (error) {
      console.error('获取监控状态失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  async function startMonitor() {
    try {
      loading.value = true
      await monitorApi.startMonitor()
      await getStatus()
      startAutoUpdate()
    } catch (error) {
      console.error('启动监控失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  async function stopMonitor() {
    try {
      loading.value = true
      await monitorApi.stopMonitor()
      await getStatus()
      stopAutoUpdate()
    } catch (error) {
      console.error('停止监控失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  return {
    status,
    loading,
    isRunning,
    progress,
    getStatus,
    startMonitor,
    stopMonitor,
    startAutoUpdate,
    stopAutoUpdate
  }
}) 
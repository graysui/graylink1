<template>
  <div class="monitor-container">
    <!-- 本地监控 -->
    <local-monitor />

    <!-- Drive Activity API 监控 -->
    <drive-activity-monitor />

    <!-- 监控日志 -->
    <el-card class="monitor-card">
      <template #header>
        <div class="card-header">
          <span>监控日志</span>
          <el-button type="primary" size="small" @click="clearLogs"> 清空日志 </el-button>
        </div>
      </template>

      <div class="log-content">
        <el-timeline>
          <el-timeline-item
            v-for="log in logs"
            :key="log.time"
            :timestamp="formatTime(log.time)"
            :type="getLogType(log.level)"
          >
            {{ log.message }}
          </el-timeline-item>
        </el-timeline>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { ElMessage } from 'element-plus'
import { formatTime } from '@/utils/time'
import { monitorApi } from '@/api/monitor'
import LocalMonitor from '@/components/monitor/LocalMonitor.vue'
import DriveActivityMonitor from '@/components/monitor/DriveActivityMonitor.vue'
import { useMonitorStore } from '@/stores/modules/monitor'
import type { MonitorLog, MonitorStats } from '@/types/monitor'

interface LogData {
  time: string
  level: 'error' | 'warning' | 'info'
  message: string
}

const logs = ref<MonitorLog[]>([])
const loading = ref(false)
const stats = ref<MonitorStats>({
  total: 0,
  success: 0,
  error: 0,
  warning: 0,
})

const monitorStore = useMonitorStore()

// 加载日志
const loadLogs = async () => {
  try {
    loading.value = true
    const { data } = await monitorApi.getLogs({ limit: 100 })
    logs.value = data.map((item: LogData) => ({
      timestamp: new Date(item.time).getTime(),
      level: item.level,
      message: item.message,
    }))
  } catch (error) {
    ElMessage.error('加载日志失败')
  } finally {
    loading.value = false
  }
}

// 清空日志
const clearLogs = async () => {
  try {
    await monitorApi.clearLogs()
    logs.value = []
    ElMessage.success('日志已清空')
  } catch (error) {
    ElMessage.error('清空日志失败')
  }
}

// 定时刷新日志
let refreshTimer: number
const startRefresh = () => {
  refreshTimer = window.setInterval(loadLogs, 10000)
}
const stopRefresh = () => {
  if (refreshTimer) {
    clearInterval(refreshTimer)
  }
}

onMounted(() => {
  loadLogs()
  startRefresh()
})

onUnmounted(() => {
  stopRefresh()
})

const getLogType = (level: MonitorLog['level']): 'primary' | 'warning' | 'danger' => {
  const map: Record<MonitorLog['level'], 'primary' | 'warning' | 'danger'> = {
    info: 'primary',
    warning: 'warning',
    error: 'danger',
  }
  return map[level]
}

const handleDataUpdate = (data: LogData[]) => {
  logs.value = data.map((item) => ({
    timestamp: new Date(item.time).getTime(),
    level: item.level,
    message: item.message,
  }))
}

const getLevelType = (level: string): 'success' | 'warning' | 'error' | 'info' => {
  const map: Record<string, 'success' | 'warning' | 'error' | 'info'> = {
    info: 'info',
    warning: 'warning',
    error: 'error',
    success: 'success',
  }
  return map[level] || 'info'
}
</script>

<style scoped lang="scss">
.monitor-container {
  padding: 20px;

  .monitor-card {
    margin-bottom: 20px;

    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .log-content {
      max-height: 400px;
      overflow-y: auto;
    }
  }
}
</style>

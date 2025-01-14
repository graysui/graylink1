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
            :key="log.timestamp"
            :timestamp="formatTime(log.timestamp)"
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
import type { LogData, MonitorState } from '@/types/monitor'

const logs = ref<LogData[]>([])
const loading = ref(false)
const autoRefresh = ref(false)
const stats = ref<MonitorState>({
  status: 'stopped',
  last_check: null,
  interval: 0,
  stats: {
    total_files: 0,
    processed_files: 0,
    pending_files: 0,
    error_count: 0,
    scan_speed: 0,
    estimated_time: 0
  },
  logs: [],
  loading: false
})

const monitorStore = useMonitorStore()

// 加载日志
const loadLogs = async () => {
  try {
    loading.value = true
    const { data } = await monitorApi.getLogs({ limit: 100 })
    logs.value = data.data.map((item: any) => ({
      timestamp: item.timestamp,
      level: item.level,
      message: item.message,
      time: new Date(item.timestamp).toISOString()
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

const getLogType = (level: LogData['level']): 'primary' | 'warning' | 'danger' => {
  const map: Record<LogData['level'], 'primary' | 'warning' | 'danger'> = {
    info: 'primary',
    warning: 'warning',
    error: 'danger',
  }
  return map[level]
}

const handleDataUpdate = (data: LogData[]) => {
  logs.value = data.map((item) => ({
    timestamp: item.timestamp,
    level: item.level,
    message: item.message,
    time: item.timestamp
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

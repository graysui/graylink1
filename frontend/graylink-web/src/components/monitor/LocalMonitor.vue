<template>
  <el-card class="monitor-card">
    <template #header>
      <div class="card-header">
        <span>本地文件监控</span>
        <div class="header-actions">
          <el-tag :type="isRunning ? 'success' : 'info'" size="small">
            {{ isRunning ? '运行中' : '已停止' }}
          </el-tag>
          <el-button-group>
            <el-button 
              type="primary" 
              size="small"
              :disabled="isRunning"
              @click="handleStart"
            >
              启动
            </el-button>
            <el-button 
              type="danger" 
              size="small"
              :disabled="!isRunning"
              @click="handleStop"
            >
              停止
            </el-button>
          </el-button-group>
        </div>
      </div>
    </template>

    <div class="monitor-content">
      <el-descriptions :column="2" border>
        <el-descriptions-item label="轮询间隔">
          {{ formatDuration(status.interval) }}
          <el-tooltip content="系统每隔这么长时间检查一次新增文件，用于补充实时监控可能漏掉的文件" placement="top">
            <el-icon class="info-icon"><InfoFilled /></el-icon>
          </el-tooltip>
        </el-descriptions-item>
        <el-descriptions-item label="上次扫描">
          {{ status.last_check ? formatTime(status.last_check) : '从未扫描' }}
        </el-descriptions-item>
      </el-descriptions>

      <div class="stats-section">
        <h4>扫描统计</h4>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-statistic title="发现新文件" :value="status.stats.total_files" />
          </el-col>
          <el-col :span="12">
            <el-statistic title="已处理文件" :value="status.stats.processed_files" />
          </el-col>
        </el-row>
      </div>
    </div>
  </el-card>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
import type { MonitorStatus } from '@/types/api'
import { monitorApi } from '@/api/monitor'
import { formatTime, formatDuration } from '@/utils/format'

const status = ref<MonitorStatus>({
  status: 'stopped',
  last_check: null,
  interval: 5000,
  stats: {
    total_files: 0,
    processed_files: 0,
    pending_files: 0,
    error_count: 0
  }
})

const isRunning = computed(() => status.value.status === 'running')
const loading = ref(false)
const refreshTimer = ref<number>()

const getStatus = async () => {
  if (loading.value) return
  try {
    loading.value = true
    const { data } = await monitorApi.getStatus()
    status.value = data
  } catch (error) {
    console.error('获取状态失败:', error)
  } finally {
    loading.value = false
  }
}

const handleStart = async () => {
  try {
    await monitorApi.start()
    await getStatus()
    ElMessage.success('监控已启动')
  } catch (error) {
    ElMessage.error('启动失败')
  }
}

const handleStop = async () => {
  try {
    await monitorApi.stop()
    await getStatus()
    ElMessage.success('监控已停止')
  } catch (error) {
    ElMessage.error('停止失败')
  }
}

const startRefresh = () => {
  stopRefresh()
  refreshTimer.value = window.setInterval(getStatus, 5000)
}

const stopRefresh = () => {
  if (refreshTimer.value) {
    clearInterval(refreshTimer.value)
    refreshTimer.value = undefined
  }
}

onMounted(() => {
  getStatus()
  startRefresh()
})

onUnmounted(() => {
  stopRefresh()
})
</script>

<style scoped lang="scss">
.monitor-card {
  margin-bottom: 20px;

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;

    .header-actions {
      display: flex;
      align-items: center;
      gap: 12px;
    }
  }

  .monitor-content {
    .stats-section {
      margin-top: 20px;
    }

    .error-section {
      margin-top: 20px;

      .el-alert {
        margin-bottom: 10px;
      }
    }

    h4 {
      margin: 0 0 12px;
      color: #606266;
    }
  }

  .info-icon {
    margin-left: 4px;
    font-size: 14px;
    color: #909399;
    cursor: help;
  }
}
</style> 
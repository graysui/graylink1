<template>
  <el-card class="monitor-card">
    <template #header>
      <div class="card-header">
        <span>本地文件监控</span>
        <div class="header-actions">
          <el-tag :type="status.running ? 'success' : 'info'" size="small">
            {{ status.running ? '运行中' : '已停止' }}
          </el-tag>
          <el-button-group>
            <el-button 
              type="primary" 
              size="small"
              :disabled="status.running"
              @click="handleStart"
            >
              启动
            </el-button>
            <el-button 
              type="danger" 
              size="small"
              :disabled="!status.running"
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
          {{ status.last_scan ? formatTime(status.last_scan) : '从未扫描' }}
        </el-descriptions-item>
      </el-descriptions>

      <div class="stats-section">
        <h4>扫描统计</h4>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-statistic title="发现新文件" :value="status.stats.new_files" />
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
import { ref, reactive, onMounted, onUnmounted } from 'vue'
import { ElMessage } from 'element-plus'
import { InfoFilled } from '@element-plus/icons-vue'
import { formatTime, formatDuration } from '@/utils/time'
import { monitorApi, type MonitorStatus } from '@/api/monitor'

// 简化状态接口
interface MonitorStatus {
  running: boolean
  interval: number
  last_scan: string | null
  stats: {
    new_files: number
    processed_files: number
  }
}

const status = reactive<MonitorStatus>({
  running: false,
  interval: 300,
  last_scan: null,
  stats: {
    new_files: 0,
    processed_files: 0
  }
})

const loading = ref(false)

// 加载监控状态
const loadStatus = async () => {
  try {
    loading.value = true
    const { data } = await monitorApi.getStatus()
    Object.assign(status, data)
  } catch (error) {
    ElMessage.error('加载状态失败')
  } finally {
    loading.value = false
  }
}

// 启动监控
const handleStart = async () => {
  try {
    await monitorApi.start()
    status.running = true
    ElMessage.success('监控已启动')
  } catch (error) {
    ElMessage.error('启动失败')
  }
}

// 停止监控
const handleStop = async () => {
  try {
    await monitorApi.stop()
    status.running = false
    ElMessage.success('监控已停止')
  } catch (error) {
    ElMessage.error('停止失败')
  }
}

// 定时刷新状态
let refreshTimer: number
const startRefresh = () => {
  refreshTimer = window.setInterval(loadStatus, 5000)
}
const stopRefresh = () => {
  if (refreshTimer) {
    clearInterval(refreshTimer)
  }
}

onMounted(() => {
  loadStatus()
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
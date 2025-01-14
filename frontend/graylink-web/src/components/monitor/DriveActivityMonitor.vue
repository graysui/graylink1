<template>
  <el-card class="monitor-card">
    <template #header>
      <div class="card-header">
        <span>Drive Activity API 监控</span>
        <div class="header-actions">
          <el-tag :type="status.enabled ? 'success' : 'info'" size="small">
            {{ status.enabled ? '已启用' : '已禁用' }}
          </el-tag>
          <el-button
            type="primary"
            size="small"
            :loading="checking"
            :disabled="!status.enabled"
            @click="handleCheck"
          >
            立即检查
          </el-button>
        </div>
      </div>
    </template>

    <div class="monitor-content">
      <el-descriptions :column="2" border>
        <el-descriptions-item label="监控状态">
          {{ status.enabled ? '运行中' : '已停止' }}
        </el-descriptions-item>
        <el-descriptions-item label="检查间隔">
          {{ formatInterval(status.check_interval) }}
        </el-descriptions-item>
        <el-descriptions-item label="上次检查">
          {{ status.last_check ? formatTime(status.last_check) : '从未检查' }}
        </el-descriptions-item>
        <el-descriptions-item label="监控文件夹">
          {{ status.folder_name || '未设置' }}
        </el-descriptions-item>
      </el-descriptions>

      <div class="stats-section" v-if="status.enabled">
        <h4>活动统计</h4>
        <el-row :gutter="20">
          <el-col :span="8">
            <el-statistic title="总活动数" :value="stats.total_activities" />
          </el-col>
          <el-col :span="8">
            <el-statistic title="已处理" :value="stats.processed_files" />
          </el-col>
          <el-col :span="8">
            <el-statistic title="处理失败" :value="stats.error_count" />
          </el-col>
        </el-row>
      </div>

      <div class="recent-activities" v-if="status.enabled && recentActivities.length > 0">
        <h4>最近活动</h4>
        <el-timeline>
          <el-timeline-item
            v-for="activity in recentActivities"
            :key="activity.time"
            :timestamp="formatTime(activity.time)"
            :type="getActivityType(activity.action_type)"
          >
            {{ formatActivity(activity) }}
          </el-timeline-item>
        </el-timeline>
      </div>
    </div>
  </el-card>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import { gdriveApi } from '@/api/gdrive'
import { formatTime } from '@/utils/time'

interface DriveActivity {
  action_type: 'create' | 'edit' | 'move'
  time: string
  file: {
    title: string
    path: string
  }
}

interface MonitorStats {
  total_activities: number
  processed_files: number
  error_count: number
}

const checking = ref(false)
const status = reactive({
  enabled: false,
  check_interval: '',
  last_check: '',
  folder_name: ''
})
const stats = reactive<MonitorStats>({
  total_activities: 0,
  processed_files: 0,
  error_count: 0
})
const recentActivities = ref<DriveActivity[]>([])

const handleCheck = async () => {
  try {
    checking.value = true
    const response = await gdriveApi.checkActivities()
    const result = response.data.data
    ElMessage.success(
      `检查完成，发现 ${result.activities} 个活动，处理了 ${result.processed} 个文件`
    )
    // 更新统计信息
    stats.total_activities += result.activities
    stats.processed_files += result.processed
    status.last_check = new Date().toISOString()
  } catch (error) {
    ElMessage.error('检查失败')
    stats.error_count++
  } finally {
    checking.value = false
  }
}

const formatInterval = (interval: string) => {
  const map: Record<string, string> = {
    '1h': '1小时',
    '6h': '6小时',
    '12h': '12小时',
    '1d': '1天',
    '7d': '7天'
  }
  return map[interval] || interval
}

const getActivityType = (type: string) => {
  const map: Record<string, 'primary' | 'success' | 'warning'> = {
    create: 'success',
    edit: 'primary',
    move: 'warning'
  }
  return map[type] || 'info'
}

const formatActivity = (activity: DriveActivity) => {
  const actionMap = {
    create: '创建了',
    edit: '修改了',
    move: '移动了'
  }
  return `${actionMap[activity.action_type]} ${activity.file.title}`
}
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

    .recent-activities {
      margin-top: 20px;
    }

    h4 {
      margin: 0 0 12px;
      color: #606266;
    }
  }
}
</style>

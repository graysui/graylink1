<template>
  <div class="emby-container">
    <!-- 服务器状态 -->
    <div class="server-status">
      <el-tag :type="serverStatus.apiStatus ? 'success' : 'warning'">
        {{ serverStatus.apiStatus ? '正常' : '异常' }}
      </el-tag>
      <span class="version">版本: {{ serverStatus.version }}</span>
      <span class="update-time">最后更新: {{ formatDateTime(serverStatus.lastUpdate) }}</span>
    </div>

    <!-- 库列表 -->
    <div class="library-list">
      <el-table :data="libraryList" style="width: 100%">
        <el-table-column prop="name" label="名称" />
        <el-table-column prop="path" label="路径" />
        <el-table-column prop="type" label="类型" />
        <el-table-column label="状态" width="200">
          <template #default="{ row }">
            <el-progress
              v-if="embyStore.refreshProgress[row.id]"
              :percentage="embyStore.refreshProgress[row.id]"
              :status="getProgressStatus(embyStore.refreshProgress[row.id])"
            />
            <el-tag v-else-if="row.refreshing" type="warning">刷新中</el-tag>
            <el-tag v-else type="success">就绪</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button @click="refreshLibrary(row)" :disabled="row.refreshing"> 刷新 </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 库详情 -->
    <div v-if="currentLibrary" class="library-detail">
      <h3>{{ currentLibrary.name }}</h3>
      <div class="info">
        <p class="path">路径: {{ currentLibrary.path }}</p>
        <p class="type">类型: {{ currentLibrary.type }}</p>
        <p class="count">项目数量: {{ currentLibrary.itemCount }}</p>
        <p class="update">最后更新: {{ formatDateTime(currentLibrary.lastUpdate) }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import type { ProgressProps } from 'element-plus'
import { useEmbyStore } from '@/stores/modules/emby'
import type { EmbyLibrary, EmbyStatus } from '@/types/emby'

const embyStore = useEmbyStore()

// 修复状态定义
const serverStatus = ref<EmbyStatus>({
  serverStatus: 'disconnected',
  apiStatus: false,
  version: undefined,
  lastCheck: undefined,
  lastUpdate: undefined
})

// 删除重复声明，使用computed
const libraryList = computed(() => embyStore.libraries)

// 当前选中的库
const currentLibrary = ref<EmbyLibrary | null>(null)

// 刷新进度状态
const getProgressStatus = (progress: number): ProgressProps['status'] => {
  return progress >= 100 ? 'success' : 'warning'
}

// 格式化时间
const formatDateTime = (time?: string) => {
  if (!time) return '未知'
  return new Date(time).toLocaleString()
}

// 计算总项目数
const totalItems = computed(() => {
  return libraryList.value.reduce((total, lib) => total + (lib.itemCount || 0), 0)
})

// 获取最后更新时间
const lastUpdateTime = computed(() => {
  const times = libraryList.value
    .map((lib) => lib.lastUpdate)
    .filter((t): t is string => t !== undefined)
  if (!times.length) return '未知'
  return formatDateTime(new Date(Math.max(...times.map(t => new Date(t).getTime()))).toISOString())
})

// 刷新指定库
const refreshLibrary = async (library: EmbyLibrary) => {
  try {
    await embyStore.refreshByPaths([library.path])
  } catch (error) {
    console.error('刷新失败:', error)
  }
}

// 刷新所有库
const refreshAllLibraries = async () => {
  try {
    await embyStore.refreshRoot()
  } catch (error) {
    console.error('刷新失败:', error)
  }
}

// 更新服务器状态
const updateServerStatus = (newStatus: EmbyStatus) => {
  serverStatus.value = newStatus
}

// 初始化
const init = async () => {
  try {
    await embyStore.checkStatus()
    await embyStore.getLibraries()
  } catch (error) {
    console.error('初始化失败:', error)
  }
}

init()
</script>

<style scoped>
.emby-container {
  padding: 20px;
}

.server-status {
  margin-bottom: 20px;
}

.library-list {
  margin-top: 20px;
}

.library-detail {
  margin-top: 20px;
  padding: 20px;
  border: 1px solid #eee;
  border-radius: 4px;
}
</style>

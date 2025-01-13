<template>
  <div class="emby-container">
    <!-- 状态概览卡片 -->
    <el-card class="status-card">
      <template #header>
        <div class="card-header">
          <span>Emby 服务状态</span>
          <el-button-group>
            <el-button
              type="primary"
              :loading="loading"
              @click="handleRefreshStatus"
            >
              刷新状态
            </el-button>
          </el-button-group>
        </div>
      </template>
      
      <el-descriptions :column="2" border>
        <el-descriptions-item label="服务器状态">
          <el-tag :type="serverStatus === 'connected' ? 'success' : 'danger'">
            {{ serverStatus === 'connected' ? '已连接' : '未连接' }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="API状态">
          <el-tag :type="apiStatus ? 'success' : 'warning'">
            {{ apiStatus ? '正常' : '异常' }}
          </el-tag>
        </el-descriptions-item>
      </el-descriptions>
    </el-card>

    <!-- 媒体库列表 -->
    <el-card class="library-card">
      <template #header>
        <div class="card-header">
          <span>媒体库列表</span>
          <el-button-group>
            <el-button
              type="primary"
              :loading="loading"
              @click="handleRefreshLibraries"
            >
              刷新列表
            </el-button>
            <el-button
              type="warning"
              :loading="loading"
              @click="handleRefreshRoot"
            >
              刷新所有
            </el-button>
          </el-button-group>
        </div>
      </template>

      <!-- 添加工具栏 -->
      <div class="toolbar">
        <el-input
          v-model="searchQuery"
          placeholder="搜索媒体库..."
          class="search-input"
          clearable
          @clear="handleSearch"
          @input="handleSearch"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>

        <el-select
          v-model="typeFilter"
          placeholder="类型筛选"
          clearable
          @change="handleFilter"
        >
          <el-option
            v-for="type in libraryTypes"
            :key="type.value"
            :label="type.label"
            :value="type.value"
          />
        </el-select>

        <el-button-group>
          <el-button
            :type="viewMode === 'table' ? 'primary' : ''"
            @click="viewMode = 'table'"
          >
            <el-icon><List /></el-icon>
          </el-button>
          <el-button
            :type="viewMode === 'grid' ? 'primary' : ''"
            @click="viewMode = 'grid'"
          >
            <el-icon><Grid /></el-icon>
          </el-button>
        </el-button-group>
      </div>

      <!-- 表格视图 -->
      <el-table
        v-if="viewMode === 'table'"
        :data="filteredLibraries"
        v-loading="loading"
      >
        <el-table-column prop="name" label="名称" />
        <el-table-column prop="path" label="路径" show-overflow-tooltip />
        <el-table-column prop="type" label="类型">
          <template #default="{ row }">
            <el-tag :type="getLibraryTagType(row.type)">
              {{ getLibraryTypeName(row.type) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="itemCount" label="项目数量" width="100" />
        <el-table-column label="刷新进度" width="200">
          <template #default="{ row }">
            <el-progress
              v-if="embyStore.refreshProgress[row.id]"
              :percentage="embyStore.refreshProgress[row.id]"
              :status="getProgressStatus(embyStore.refreshProgress[row.id])"
            />
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button-group>
              <el-button
                size="small"
                type="primary"
                @click="handleRefreshLibrary(row)"
              >
                刷新
              </el-button>
              <el-button
                size="small"
                type="info"
                @click="handleViewDetail(row)"
              >
                详情
              </el-button>
            </el-button-group>
          </template>
        </el-table-column>
      </el-table>

      <!-- 网格视图 -->
      <div v-else class="library-grid">
        <el-card
          v-for="library in filteredLibraries"
          :key="library.id"
          class="library-card-grid"
          :body-style="{ padding: '0px' }"
        >
          <div class="library-card-header">
            <el-tag :type="getLibraryTagType(library.type)">
              {{ getLibraryTypeName(library.type) }}
            </el-tag>
            <h3>{{ library.name }}</h3>
          </div>
          <div class="library-card-content">
            <p class="path">{{ library.path }}</p>
            <p class="count">项目数量: {{ library.itemCount }}</p>
            <p class="update">最后更新: {{ formatDateTime(library.lastUpdate) }}</p>
          </div>
          <div class="library-card-actions">
            <el-button-group>
              <el-button
                size="small"
                type="primary"
                @click="handleRefreshLibrary(library)"
              >
                刷新
              </el-button>
              <el-button
                size="small"
                type="info"
                @click="handleViewDetail(library)"
              >
                详情
              </el-button>
            </el-button-group>
          </div>
        </el-card>
      </div>
    </el-card>

    <!-- 进度条 -->
    <progress-bar
      v-if="showProgress"
      :title="progressTitle"
      :current="progressCurrent"
      :total="progressTotal"
      :detail="progressDetail"
    />

    <!-- 确认对话框 -->
    <el-dialog
      v-model="showConfirmDialog"
      :title="confirmDialogTitle"
      width="30%"
    >
      <span>{{ confirmDialogMessage }}</span>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showConfirmDialog = false">取消</el-button>
          <el-button
            type="primary"
            :loading="confirmLoading"
            @click="handleConfirm"
          >
            确认
          </el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 详情对话框 -->
    <el-dialog
      v-model="showDetailDialog"
      title="媒体库详情"
      width="50%"
    >
      <el-descriptions :column="1" border>
        <el-descriptions-item label="名称">
          {{ currentLibrary?.name }}
        </el-descriptions-item>
        <el-descriptions-item label="路径">
          {{ currentLibrary?.path }}
        </el-descriptions-item>
        <el-descriptions-item label="类型">
          {{ currentLibrary?.type }}
        </el-descriptions-item>
        <el-descriptions-item label="项目数量">
          {{ currentLibrary?.itemCount }}
        </el-descriptions-item>
        <el-descriptions-item label="最后更新">
          {{ formatDateTime(currentLibrary?.lastUpdate) }}
        </el-descriptions-item>
      </el-descriptions>
    </el-dialog>

    <!-- 媒体库统计卡片 -->
    <el-card class="stats-card">
      <template #header>
        <div class="card-header">
          <span>媒体库统计</span>
        </div>
      </template>
      
      <el-row :gutter="20">
        <el-col :span="8">
          <el-statistic title="媒体库总数" :value="libraries.length">
            <template #suffix>个</template>
          </el-statistic>
        </el-col>
        <el-col :span="8">
          <el-statistic 
            title="总项目数" 
            :value="totalItems"
            :value-style="{ color: '#409EFF' }"
          >
            <template #suffix>个</template>
          </el-statistic>
        </el-col>
        <el-col :span="8">
          <el-statistic 
            title="最近更新" 
            :value="lastUpdateTime"
            :value-style="{ fontSize: '14px' }"
          />
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch, computed } from 'vue'
import { useEmbyStore } from '@/stores/modules/emby'
import { ElMessage } from 'element-plus'
import ProgressBar from '@/components/common/ProgressBar.vue'
import { formatDateTime } from '@/utils/format'
import type { EmbyLibrary } from '@/types/api'
import { Search, List, Grid } from '@element-plus/icons-vue'

const embyStore = useEmbyStore()
const loading = ref(false)
const serverStatus = ref('disconnected')
const apiStatus = ref(false)

// 进度条相关
const showProgress = ref(false)
const progressTitle = ref('')
const progressCurrent = ref(0)
const progressTotal = ref(0)
const progressDetail = ref('')

// 确认对话框相关
const showConfirmDialog = ref(false)
const confirmDialogTitle = ref('')
const confirmDialogMessage = ref('')
const confirmLoading = ref(false)
const confirmAction = ref<() => Promise<void>>()

// 详情对话框相关
const showDetailDialog = ref(false)
const currentLibrary = ref<EmbyLibrary | null>(null)

// 计算属性
const libraries = computed(() => embyStore.libraries)

const totalItems = computed(() => {
  return libraries.value.reduce((total, lib) => total + (lib.itemCount || 0), 0)
})

const lastUpdateTime = computed(() => {
  const times = libraries.value
    .map(lib => lib.lastUpdate)
    .filter(Boolean) as string[]
  
  if (times.length === 0) return '暂无更新'
  
  const latestTime = new Date(Math.max(...times.map(t => new Date(t).getTime())))
  return formatDateTime(latestTime)
})

// 方法
const handleRefreshStatus = async () => {
  try {
    loading.value = true
    await embyStore.checkStatus()
    serverStatus.value = 'connected'
    apiStatus.value = true
  } catch (err) {
    handleError(err, '获取服务器状态失败')
  } finally {
    loading.value = false
  }
}

const handleRefreshLibrary = (library: EmbyLibrary) => {
  confirmDialogTitle.value = '刷新媒体库'
  confirmDialogMessage.value = `确定要刷新媒体库 "${library.name}" 吗？`
  confirmAction.value = async () => {
    try {
      confirmLoading.value = true
      await embyStore.refreshByPaths([library.path], library.id)
      ElMessage.success('媒体库刷新成功')
    } catch (err) {
      handleError(err, '媒体库刷新失败')
    } finally {
      confirmLoading.value = false
      showConfirmDialog.value = false
    }
  }
  showConfirmDialog.value = true
}

const handleViewDetail = (library: EmbyLibrary) => {
  currentLibrary.value = library
  showDetailDialog.value = true
}

const handleConfirm = async () => {
  if (confirmAction.value) {
    await confirmAction.value()
  }
}

// 更新进度相关方法
const updateProgress = (title: string, current: number, total: number, detail?: string) => {
  showProgress.value = true
  progressTitle.value = title
  progressCurrent.value = current
  progressTotal.value = total
  progressDetail.value = detail || ''
}

const resetProgress = () => {
  showProgress.value = false
  progressTitle.value = ''
  progressCurrent.value = 0
  progressTotal.value = 0
  progressDetail.value = ''
}

// 错误处理方法
const handleError = (err: unknown, message: string) => {
  console.error(message, err)
  ElMessage.error(message)
  resetProgress()
}

// 添加刷新媒体库列表方法
const handleRefreshLibraries = async () => {
  try {
    loading.value = true
    await embyStore.getLibraries()
    ElMessage.success('媒体库列表刷新成功')
  } catch (err) {
    handleError(err, '获取媒体库列表失败')
  } finally {
    loading.value = false
  }
}

// 添加刷新所有媒体库方法
const handleRefreshRoot = () => {
  confirmDialogTitle.value = '刷新所有媒体库'
  confirmDialogMessage.value = '确定要刷新所有媒体库吗？此操作可能需要较长时间。'
  confirmAction.value = async () => {
    try {
      confirmLoading.value = true
      updateProgress('刷新媒体库', 0, 100)
      
      await embyStore.refreshRoot()
      
      updateProgress('刷新媒体库', 100, 100, '操作完成')
      ElMessage.success('所有媒体库刷新成功')
    } catch (err) {
      handleError(err, '刷新媒体库失败')
    } finally {
      confirmLoading.value = false
      showConfirmDialog.value = false
      setTimeout(resetProgress, 2000)
    }
  }
  showConfirmDialog.value = true
}

// 添加状态监听
watch(() => embyStore.status, (newStatus) => {
  serverStatus.value = newStatus.serverStatus
  apiStatus.value = newStatus.apiStatus
}, { immediate: true })

// 添加自动刷新功能
const autoRefreshInterval = ref<number | null>(null)

const startAutoRefresh = () => {
  stopAutoRefresh()
  autoRefreshInterval.value = window.setInterval(() => {
    if (!loading.value) {
      handleRefreshStatus()
    }
  }, 30000) // 每30秒刷新一次状态
}

const stopAutoRefresh = () => {
  if (autoRefreshInterval.value) {
    clearInterval(autoRefreshInterval.value)
    autoRefreshInterval.value = null
  }
}

// 在组件挂载时启动自动刷新，卸载时停止
onMounted(() => {
  handleRefreshStatus()
  handleRefreshLibraries()
  startAutoRefresh()
})

onUnmounted(() => {
  stopAutoRefresh()
})

// 添加媒体库类型处理方法
const getLibraryTagType = (type: string) => {
  const typeMap: Record<string, string> = {
    'movies': 'success',
    'tvshows': 'warning',
    'music': 'info',
    'photos': 'primary',
    'default': ''
  }
  return typeMap[type.toLowerCase()] || typeMap.default
}

const getLibraryTypeName = (type: string) => {
  const nameMap: Record<string, string> = {
    'movies': '电影',
    'tvshows': '电视剧',
    'music': '音乐',
    'photos': '照片',
    'default': '其他'
  }
  return nameMap[type.toLowerCase()] || type
}

// 视图模式
const viewMode = ref<'table' | 'grid'>('table')

// 搜索和筛选
const searchQuery = ref('')
const typeFilter = ref('')

const libraryTypes = [
  { label: '电影', value: 'movies' },
  { label: '电视剧', value: 'tvshows' },
  { label: '音乐', value: 'music' },
  { label: '照片', value: 'photos' }
]

// 筛选后的媒体库列表
const filteredLibraries = computed(() => {
  let result = libraries.value

  // 搜索过滤
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(lib => 
      lib.name.toLowerCase().includes(query) ||
      lib.path.toLowerCase().includes(query)
    )
  }

  // 类型过滤
  if (typeFilter.value) {
    result = result.filter(lib => 
      lib.type.toLowerCase() === typeFilter.value.toLowerCase()
    )
  }

  return result
})

// 搜索处理
const handleSearch = () => {
  // 可以添加防抖处理
  // 这里简单处理，实际项目中建议使用 lodash 的 debounce
}

// 筛选处理
const handleFilter = () => {
  // 可以添加额外的筛选逻辑
}

const getProgressStatus = (progress: number) => {
  if (progress >= 100) return 'success'
  if (progress > 0) return ''
  return 'exception'
}
</script>

<style scoped lang="scss">
.emby-container {
  padding: 20px;
  
  .status-card,
  .stats-card,
  .library-card {
    margin-bottom: 20px;
  }
  
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
}

.dialog-footer {
  padding-top: 20px;
  text-align: right;
}

.toolbar {
  margin-bottom: 16px;
  display: flex;
  gap: 16px;
  align-items: center;

  .search-input {
    width: 300px;
  }
}

.library-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 16px;
  margin-top: 16px;

  .library-card-grid {
    .library-card-header {
      padding: 12px;
      border-bottom: 1px solid #eee;
      
      h3 {
        margin: 8px 0 0;
      }
    }

    .library-card-content {
      padding: 12px;
      
      .path {
        color: #666;
        font-size: 14px;
        margin: 8px 0;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      }
      
      .count {
        font-size: 14px;
        margin: 4px 0;
      }
      
      .update {
        font-size: 12px;
        color: #999;
        margin: 4px 0;
      }
    }

    .library-card-actions {
      padding: 12px;
      border-top: 1px solid #eee;
      text-align: right;
    }
  }
}
</style> 
<template>
  <div class="symlink-manager">
    <!-- 添加错误提示 -->
    <error-alert
      :error="error"
      @clear="error = null"
      class="error-alert"
    />
    
    <!-- 工具栏 -->
    <el-card class="toolbar">
      <el-row :gutter="20">
        <el-col :span="24" class="toolbar-buttons">
          <el-button-group>
            <el-button
              type="primary"
              :icon="Refresh"
              :loading="loading"
              @click="handleVerify"
            >
              验证软链接
            </el-button>
            <el-button
              type="success"
              :icon="Check"
              :loading="loading"
              @click="handleRebuild"
            >
              重建软链接
            </el-button>
            <el-button
              type="danger"
              :icon="Delete"
              :loading="loading"
              @click="handleClear"
            >
              清理软链接
            </el-button>
          </el-button-group>
        </el-col>
      </el-row>
    </el-card>

    <!-- 验证结果 -->
    <el-card v-loading="loading" class="verify-result" element-loading-text="正在验证软链接...">
      <template #header>
        <div class="card-header">
          <span>验证结果</span>
          <el-button
            type="primary"
            link
            :icon="Download"
            @click="exportResult"
          >
            导出结果
          </el-button>
        </div>
      </template>

      <!-- 无效软链接列表 -->
      <div v-if="verifyResult.broken_links.length" class="result-section">
        <h4>
          <el-tag type="danger">无效软链接</el-tag>
          <span class="count">({{ verifyResult.broken_links.length }})</span>
        </h4>
        <el-table :data="verifyResult.broken_links" style="width: 100%">
          <el-table-column prop="path" label="路径" min-width="300" />
          <el-table-column label="操作" width="150" fixed="right">
            <template #default="{ row }">
              <el-button
                type="danger"
                size="small"
                :icon="Delete"
                @click="handleRemove(row)"
              >
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <!-- 无效目标列表 -->
      <div v-if="verifyResult.invalid_targets.length" class="result-section">
        <h4>
          <el-tag type="warning">无效目标</el-tag>
          <span class="count">({{ verifyResult.invalid_targets.length }})</span>
        </h4>
        <el-table :data="verifyResult.invalid_targets" style="width: 100%">
          <el-table-column prop="path" label="路径" min-width="300" />
          <el-table-column label="操作" width="150" fixed="right">
            <template #default="{ row }">
              <el-button
                type="primary"
                size="small"
                :icon="Link"
                @click="handleRecreate(row)"
              >
                重新创建
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <!-- 无问题提示 -->
      <el-empty
        v-if="!verifyResult.broken_links.length && !verifyResult.invalid_targets.length"
        description="未发现问题"
      />

      <!-- 空状态 -->
      <el-empty
        v-if="!verifyResult"
        description="请点击验证按钮开始检查"
      />
    </el-card>

    <!-- 添加进度显示 -->
    <el-card v-if="showProgress" class="progress-card">
      <template #header>
        <div class="card-header">
          <span>操作进度</span>
        </div>
      </template>
      <progress-bar
        :title="progressTitle"
        :current="progressCurrent"
        :total="progressTotal"
        :detail="progressDetail"
      />
    </el-card>

    <!-- 添加统计信息 -->
    <el-card class="stats-card">
      <template #header>
        <div class="card-header">
          <span>统计信息</span>
        </div>
      </template>
      <el-row :gutter="20">
        <el-col :span="8">
          <el-statistic title="软链接总数" :value="stats.total" />
        </el-col>
        <el-col :span="8">
          <el-statistic title="无效软链接" :value="stats.broken" />
        </el-col>
        <el-col :span="8">
          <el-statistic title="无效目标" :value="stats.invalid" />
        </el-col>
      </el-row>
    </el-card>

    <!-- 操作确认对话框 -->
    <el-dialog
      v-model="showConfirmDialog"
      :title="confirmDialogTitle"
      width="400px"
    >
      <p>{{ confirmDialogMessage }}</p>
      <template #footer>
        <el-button @click="showConfirmDialog = false">取消</el-button>
        <el-button
          type="primary"
          :loading="confirmLoading"
          @click="confirmAction"
        >
          确定
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { storeToRefs } from 'pinia'
import { ElMessage } from 'element-plus'
import {
  Refresh,
  Check,
  Delete,
  Download,
  Link,
  Edit,
  Plus,
  Search,
  Warning
} from '@element-plus/icons-vue'
import { useSymlinkStore } from '@/stores/modules/symlink'
import ErrorAlert from '@/components/common/ErrorAlert.vue'
import ProgressBar from '@/components/common/ProgressBar.vue'
import { useIntervalFn } from '@/composables/useIntervalFn'
import type { VerifyResult } from '@/types/api'
import { showSuccess, showError } from '@/utils/message'

defineOptions({
  name: 'SymlinkManagerPage'
})

const symlinkStore = useSymlinkStore()
const { loading } = storeToRefs(symlinkStore)

// 确认对话框状态
const showConfirmDialog = ref(false)
const confirmLoading = ref(false)
const confirmAction = ref<() => Promise<void>>(() => Promise.resolve())
const confirmDialogTitle = ref('')
const confirmDialogMessage = ref('')

// 添加错误状态
const error = ref<Error | null>(null)

// 添加进度状态
const showProgress = ref(false)
const progressTitle = ref('')
const progressCurrent = ref(0)
const progressTotal = ref(0)
const progressDetail = ref('')

// 添加自动刷新
const { pause, resume } = useIntervalFn(async () => {
  if (showProgress.value) {
    await handleVerify()
  }
}, 5000)

// 修改更新进度函数
const updateProgress = (title: string, current: number, total: number, detail?: string) => {
  showProgress.value = true
  progressTitle.value = title
  progressCurrent.value = current
  progressTotal.value = total
  progressDetail.value = detail || ''
  resume() // 开始自动刷新
}

// 修改重置进度函数
const resetProgress = () => {
  showProgress.value = false
  progressCurrent.value = 0
  progressTotal.value = 0
  progressDetail.value = ''
  pause() // 停止自动刷新
}

// 页面卸载时清理
onUnmounted(() => {
  pause()
})

// 验证软链接
const handleVerify = async () => {
  try {
    await symlinkStore.verifySymlinks()
  } catch (err) {
    error.value = err as Error
  }
}

// 修改错误处理
const handleError = (err: unknown, message: string) => {
  error.value = err instanceof Error ? err : new Error(message)
  ElMessage.error(message)
  resetProgress()
}

// 修改重建软链接函数
const handleRebuild = () => {
  confirmDialogTitle.value = '重建软链接'
  confirmDialogMessage.value = '确定要重建所有软链接吗？此操作可能需要一些时间。'
  confirmAction.value = async () => {
    try {
      confirmLoading.value = true
      updateProgress('重建软链接', 0, 100)
      
      const result = await symlinkStore.rebuildSymlinks()
      
      updateProgress('重建软链接', 100, 100, '操作完成')
      setTimeout(resetProgress, 2000)
      
      showSuccess('软链接重建完成')
      await handleVerify()
    } catch (err) {
      showError('软链接重建失败')
    } finally {
      confirmLoading.value = false
      showConfirmDialog.value = false
    }
  }
  showConfirmDialog.value = true
}

// 清理软链接
const handleClear = () => {
  confirmDialogTitle.value = '清理软链接'
  confirmDialogMessage.value = '确定要清理所有软链接吗？此操作不可恢复。'
  confirmAction.value = async () => {
    try {
      confirmLoading.value = true
      await symlinkStore.clearSymlinks()
      showSuccess('软链接清理完成')
      await handleVerify()
    } catch (error) {
      ElMessage.error('软链接清理失败')
    } finally {
      confirmLoading.value = false
      showConfirmDialog.value = false
    }
  }
  showConfirmDialog.value = true
}

// 删除单个软链接
const handleRemove = (link: string) => {
  confirmDialogTitle.value = '删除软链接'
  confirmDialogMessage.value = `确定要删除软链接 ${link} 吗？`
  confirmAction.value = async () => {
    try {
      confirmLoading.value = true
      await symlinkStore.removeSymlink(link)
      showSuccess('软链接删除成功')
      await handleVerify()
    } catch (error) {
      ElMessage.error('软链接删除失败')
    } finally {
      confirmLoading.value = false
      showConfirmDialog.value = false
    }
  }
  showConfirmDialog.value = true
}

// 重新创建软链接
const handleRecreate = (target: string) => {
  confirmDialogTitle.value = '重新创建软链接'
  confirmDialogMessage.value = `确定要重新创建指向 ${target} 的软链接吗？`
  confirmAction.value = async () => {
    try {
      confirmLoading.value = true
      await symlinkStore.createSymlink(target)
      showSuccess('软链接创建成功')
      await handleVerify()
    } catch (error) {
      ElMessage.error('软链接创建失败')
    } finally {
      confirmLoading.value = false
      showConfirmDialog.value = false
    }
  }
  showConfirmDialog.value = true
}

// 导出验证结果
const exportResult = () => {
  if (!verifyResult.value) return
  
  const result = {
    broken_links: verifyResult.value.broken_links,
    invalid_targets: verifyResult.value.invalid_targets,
    timestamp: new Date().toISOString()
  }
  
  const blob = new Blob([JSON.stringify(result, null, 2)], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = `symlink-verify-result-${new Date().toISOString()}.json`
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  URL.revokeObjectURL(url)
}

// 添加统计计算
const stats = computed(() => {
  if (!verifyResult.value) {
    return {
      total: 0,
      broken: 0,
      invalid: 0
    }
  }
  
  return {
    total: verifyResult.value.broken_links.length + verifyResult.value.invalid_targets.length,
    broken: verifyResult.value.broken_links.length,
    invalid: verifyResult.value.invalid_targets.length
  }
})

// 页面加载时验证软链接
onMounted(async () => {
  await handleVerify()
})

// 使用计算属性处理 null 情况
const verifyResult = computed<VerifyResult>(() => symlinkStore.verifyResult || {
  broken_links: [],
  invalid_targets: [],
  timestamp: new Date().toISOString(),
  stats: {
    total: 0,
    broken: 0,
    invalid: 0
  }
})

// 定义图标对象
const icons = {
  Refresh,
  Check,
  Delete,
  Download,
  Link,
  Edit,
  Plus,
  Search,
  Warning
} as const
</script>

<style scoped lang="scss">
.symlink-manager {
  padding: 20px;
  
  .error-alert {
    margin-bottom: 20px;
  }
  
  .toolbar {
    margin-bottom: 20px;
    
    .toolbar-buttons {
      text-align: right;
    }
  }
  
  .verify-result {
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    
    .result-section {
      margin-bottom: 20px;
      
      h4 {
        margin: 10px 0;
        display: flex;
        align-items: center;
        
        .count {
          margin-left: 8px;
          color: #666;
        }
      }
    }
  }
  
  .progress-card {
    margin-bottom: 20px;
  }
  
  .stats-card {
    margin-bottom: 20px;
  }
}
</style> 
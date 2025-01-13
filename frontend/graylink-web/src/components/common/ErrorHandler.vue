<template>
  <el-dialog
    v-model="visible"
    title="错误提示"
    width="500px"
  >
    <div class="error-content">
      <el-alert
        :title="error?.message || '未知错误'"
        type="error"
        :description="error?.stack"
        show-icon
      />
    </div>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="handleClose">关闭</el-button>
        <el-button type="primary" @click="handleRetry">
          重试
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useErrorStore } from '@/stores/modules/error'

const errorStore = useErrorStore()

const visible = computed({
  get: () => !!errorStore.error,
  set: (value) => {
    if (!value) errorStore.clearError()
  }
})

const error = computed(() => errorStore.error)

const handleClose = () => {
  errorStore.clearError()
}

const handleRetry = () => {
  // 实现重试逻辑
  window.location.reload()
}
</script>

<style scoped>
.error-stack {
  margin: 8px 0 0;
  font-size: 12px;
  white-space: pre-wrap;
  word-break: break-all;
}
</style> 
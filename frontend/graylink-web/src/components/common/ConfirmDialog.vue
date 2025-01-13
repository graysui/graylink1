<template>
  <el-dialog
    v-model="dialogVisible"
    :title="title"
    width="400px"
    :close-on-click-modal="false"
  >
    <div class="dialog-content">
      {{ message }}
    </div>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="handleCancel">取消</el-button>
        <el-button
          type="primary"
          :loading="loading"
          @click="handleConfirm"
        >
          确定
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const props = defineProps<{
  title: string
  message: string
  loading?: boolean
}>()

const emit = defineEmits<{
  (e: 'confirm'): void
  (e: 'cancel'): void
  (e: 'update:loading', value: boolean): void
}>()

const dialogVisible = ref(false)

const handleConfirm = () => {
  emit('confirm')
}

const handleCancel = () => {
  emit('cancel')
  dialogVisible.value = false
}

defineExpose({
  show: () => {
    dialogVisible.value = true
  },
  hide: () => {
    dialogVisible.value = false
  }
})
</script> 
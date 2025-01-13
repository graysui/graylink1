<template>
  <el-alert
    v-if="error"
    :title="error.message || '操作失败'"
    type="error"
    show-icon
    closable
    @close="clearError"
  />
</template>

<script setup lang="ts">
defineProps<{
  error: Error | null
}>()

const emit = defineEmits<{
  (e: 'clear'): void
}>()

const clearError = () => {
  emit('clear')
}
</script> 
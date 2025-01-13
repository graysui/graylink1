<template>
  <div class="progress-container">
    <el-progress
      :percentage="percentage"
      :status="status"
      :stroke-width="8"
      :text-inside="true"
    >
      <template #default="{ percentage }">
        <span>{{ percentage }}%</span>
        <span v-if="detail" class="progress-detail">{{ detail }}</span>
      </template>
    </el-progress>
  </div>
</template>

<script setup lang="ts">
import type { ProgressProps } from 'element-plus'

defineProps<{
  percentage: number
  status?: ProgressProps['status']
  title?: string
  detail?: string
}>()
</script>

<style scoped>
.progress-container {
  margin: 10px 0;
}

.progress-detail {
  margin-left: 10px;
  font-size: 12px;
  color: #909399;
}
</style> 
<template>
  <div class="progress-container">
    <el-progress
      :percentage="computedPercentage"
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
import { computed } from 'vue'
import type { ProgressProps } from 'element-plus'

interface Props {
  current?: number
  total?: number
  percentage?: number
  status?: ProgressProps['status']
  title?: string
  detail?: string
}

const props = withDefaults(defineProps<Props>(), {
  current: 0,
  total: 0,
  percentage: 0
})

// 计算百分比
const computedPercentage = computed(() => {
  if (props.percentage) return props.percentage
  if (!props.total) return 0
  return Math.round((props.current / props.total) * 100)
})
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

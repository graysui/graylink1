<template>
  <div class="status-indicator">
    <el-tag
      :type="statusType"
      :effect="effect"
      size="small"
    >
      {{ statusText }}
    </el-tag>
    <el-tooltip
      v-if="detail"
      :content="detail"
      placement="top"
    >
      <el-icon class="info-icon"><InfoFilled /></el-icon>
    </el-tooltip>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { InfoFilled } from '@element-plus/icons-vue'
import type { TagProps } from 'element-plus'

const props = defineProps<{
  status: string
  text?: string
  detail?: string
  effect?: 'light' | 'dark' | 'plain'
}>()

const statusType = computed<TagProps['type']>(() => {
  switch (props.status) {
    case 'success': return 'success'
    case 'warning': return 'warning'
    case 'error': return 'danger'
    default: return 'info'
  }
})
const statusText = computed(() => props.text || props.status)
</script>

<style scoped>
.status-indicator {
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.info-icon {
  font-size: 14px;
  color: #909399;
  cursor: pointer;
}
</style> 
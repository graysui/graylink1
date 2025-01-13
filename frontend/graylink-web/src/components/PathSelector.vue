<template>
  <div class="path-selector">
    <el-input
      v-model="localValue"
      :placeholder="placeholder"
      @change="handleSelect"
    >
      <template #append>
        <el-button>
          <el-icon><Fold /></el-icon>
          选择
        </el-button>
      </template>
    </el-input>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { Fold } from '@element-plus/icons-vue'
import type { DirListItem } from '@/types/api'

const props = defineProps<{
  modelValue: string
  rootPath?: string
  placeholder?: string
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void
}>()

const currentPath = ref(props.modelValue)
const localValue = ref(props.modelValue)

// 简化组件，移除目录操作功能
const handleSelect = () => {
  emit('update:modelValue', currentPath.value)
}

watch(() => props.modelValue, (val) => {
  currentPath.value = val
  localValue.value = val
})
</script>

<style scoped lang="scss">
.path-selector {
  .path-browser {
    .current-path {
      margin-bottom: 16px;
      padding: 8px;
      background-color: #f5f7fa;
      border-radius: 4px;
    }

    .create-dir {
      margin-top: 16px;
    }
  }
}

:deep(.el-breadcrumb__item) {
  cursor: pointer;
}
</style> 
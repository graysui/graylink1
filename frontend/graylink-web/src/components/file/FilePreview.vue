<template>
  <el-dialog
    v-model="visible"
    :title="fileName"
    width="80%"
    class="file-preview-dialog"
  >
    <!-- 图片预览 -->
    <div v-if="isImage" class="preview-content image-preview">
      <el-image :src="fileUrl" fit="contain" />
    </div>

    <!-- 视频预览 -->
    <div v-else-if="isVideo" class="preview-content video-preview">
      <video controls :src="fileUrl" style="width: 100%">
        您的浏览器不支持视频预览
      </video>
    </div>

    <!-- 文本预览 -->
    <div v-else-if="isText" class="preview-content text-preview">
      <el-scrollbar height="400px">
        <pre>{{ textContent }}</pre>
      </el-scrollbar>
    </div>

    <!-- 其他文件 -->
    <div v-else class="preview-content other-preview">
      <el-empty description="暂不支持该类型文件预览" />
    </div>

    <!-- 文件信息 -->
    <template #footer>
      <el-descriptions :column="3" border>
        <el-descriptions-item label="文件大小">
          {{ formatFileSize(fileInfo.size) }}
        </el-descriptions-item>
        <el-descriptions-item label="修改时间">
          {{ formatDateTime(fileInfo.modified_time) }}
        </el-descriptions-item>
        <el-descriptions-item label="文件类型">
          {{ fileType }}
        </el-descriptions-item>
      </el-descriptions>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import type { FileRecord } from '@/types/api'

const props = defineProps<{
  modelValue: boolean
  fileInfo: FileRecord
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: boolean): void
}>()

// 控制对话框显示
const visible = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

// 文件名
const fileName = computed(() => {
  return props.fileInfo.path.split('/').pop() || props.fileInfo.path
})

// 文件类型判断
const fileType = computed(() => {
  const name = fileName.value.toLowerCase()
  if (/\.(jpg|jpeg|png|gif|webp)$/.test(name)) return '图片'
  if (/\.(mp4|webm|mkv)$/.test(name)) return '视频'
  if (/\.(txt|log|md|json|yml|yaml|xml|html|css|js|ts)$/.test(name)) return '文本'
  return '其他'
})

const isImage = computed(() => fileType.value === '图片')
const isVideo = computed(() => fileType.value === '视频')
const isText = computed(() => fileType.value === '文本')

// 文件URL（实际项目中需要从后端获取）
const fileUrl = computed(() => {
  return `/api/file/preview/${encodeURIComponent(props.fileInfo.path)}`
})

// 文本内容（实际项目中需要从后端获取）
const textContent = ref('')

// 格式化函数
const formatFileSize = (bytes: number) => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return `${(bytes / Math.pow(k, i)).toFixed(2)} ${sizes[i]}`
}

const formatDateTime = (dateStr: string) => {
  const date = new Date(dateStr)
  return date.toLocaleString()
}
</script>

<style scoped lang="scss">
.file-preview-dialog {
  :deep(.el-dialog__body) {
    padding: 0;
  }

  .preview-content {
    min-height: 400px;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #f5f7fa;
    
    &.image-preview {
      :deep(.el-image) {
        max-height: 600px;
      }
    }
    
    &.text-preview {
      pre {
        margin: 0;
        padding: 16px;
        font-family: monospace;
        white-space: pre-wrap;
        word-wrap: break-word;
      }
    }
  }
}
</style> 
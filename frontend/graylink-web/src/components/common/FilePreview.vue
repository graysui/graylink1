<template>
  <el-dialog
    v-model="visible"
    :title="fileName"
    width="800px"
    class="file-preview"
    destroy-on-close
    @update:modelValue="emit('update:visible', $event)"
  >
    <!-- 预览内容 -->
    <div class="preview-content">
      <!-- 图片预览 -->
      <div v-if="isImage" class="preview-image">
        <el-image
          :src="fileUrl"
          fit="contain"
          :preview-src-list="fileUrl ? [fileUrl] : []"
        />
      </div>

      <!-- 视频预览 -->
      <div v-else-if="isVideo" class="preview-video">
        <video
          controls
          :src="fileUrl"
          class="video-player"
        />
      </div>

      <!-- 文本预览 -->
      <div v-else-if="isText" class="preview-text">
        <el-scrollbar height="400px">
          <pre><code>{{ fileContent }}</code></pre>
        </el-scrollbar>
      </div>

      <!-- 其他文件 -->
      <div v-else class="preview-other">
        <el-empty description="暂不支持预览此类型文件" />
      </div>
    </div>

    <!-- 文件信息 -->
    <div class="file-info">
      <el-descriptions :column="2" border>
        <el-descriptions-item label="文件名">
          {{ fileName }}
        </el-descriptions-item>
        <el-descriptions-item label="文件大小">
          {{ formatFileSize(fileSize) }}
        </el-descriptions-item>
        <el-descriptions-item label="修改时间">
          {{ formatTime(modifiedTime) }}
        </el-descriptions-item>
      </el-descriptions>
    </div>

    <!-- 操作按钮 -->
    <template #footer>
      <el-button @click="emit('update:visible', false)">
        关闭
      </el-button>
      <el-button
        type="primary"
        :icon="Download"
        @click="handleDownload"
      >
        下载
      </el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { Download } from '@element-plus/icons-vue'
import { formatFileSize, formatTime } from '@/utils/format'
import type { FileInfo } from '@/types/api'
import { ElMessage } from 'element-plus'

const props = defineProps<{
  fileInfo: FileInfo
  visible: boolean
}>()

const emit = defineEmits<{
  (e: 'update:visible', value: boolean): void
}>()

// 状态
const previewLoading = ref(false)
const previewError = ref<Error | null>(null)
const fileContent = ref('')

// 计算属性
const fileName = computed(() => props.fileInfo.name)
const fileSize = computed(() => props.fileInfo.size)
const modifiedTime = computed(() => props.fileInfo.modified_time)
const fileUrl = computed(() => {
  return props.fileInfo.preview_url || props.fileInfo.download_url || ''
})

// 文件类型判断
const isImage = computed(() => /\.(jpg|jpeg|png|gif|webp)$/i.test(props.fileInfo.name))
const isVideo = computed(() => /\.(mp4|webm|mkv)$/i.test(props.fileInfo.name))
const isText = computed(() => /\.(txt|log|md|json|yml|yaml|xml|html|css|js|ts)$/i.test(props.fileInfo.name))

// 下载文件
const handleDownload = async () => {
  if (!fileUrl.value) {
    ElMessage.error('文件链接不存在')
    return
  }
  try {
    const response = await fetch(fileUrl.value)
    const blob = await response.blob()
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = fileName.value
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
  } catch (error) {
    console.error('下载文件失败:', error)
    ElMessage.error('下载文件失败')
  }
}
</script>

<style scoped lang="scss">
.file-preview {
  :deep(.el-dialog__body) {
    padding: 0;
  }

  .preview-content {
    min-height: 400px;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: #f5f7fa;
    padding: 20px;
  }

  .preview-image,
  .preview-video,
  .preview-text,
  .preview-other {
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .file-info {
    padding: 20px;
    border-top: 1px solid #eee;
  }
}
</style> 
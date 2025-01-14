<template>
  <el-dialog
    v-model="dialogVisible"
    title="上传文件"
    width="500px"
  >
    <el-upload
      class="upload-demo"
      :action="uploadUrl"
      :headers="headers"
      :data="uploadData"
      :multiple="true"
      :on-success="handleSuccess"
      :on-error="handleError"
      drag
    >
      <el-icon class="el-icon--upload"><Upload /></el-icon>
      <div class="el-upload__text">
        拖拽文件到此处或 <em>点击上传</em>
      </div>
    </el-upload>
  </el-dialog>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { Upload } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const props = defineProps<{
  modelValue: boolean
  currentPath: string
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: boolean): void
  (e: 'success'): void
}>()

const dialogVisible = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const uploadUrl = '/api/files/upload'
const headers = {
  // 如果需要认证token等，在这里添加
}
const uploadData = computed(() => ({
  path: props.currentPath
}))

const handleSuccess = () => {
  ElMessage.success('上传成功')
  emit('success')
}

const handleError = () => {
  ElMessage.error('上传失败')
}
</script>

<style scoped>
.upload-demo {
  text-align: center;
}
</style>

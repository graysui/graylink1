<template>
  <div class="path-selector">
    <el-input
      v-model="localValue"
      :placeholder="placeholder"
      class="path-input"
      @change="handleChange"
    >
      <template #append>
        <el-button @click="handleSelect">
          <el-icon><Folder /></el-icon>
          选择
        </el-button>
      </template>
    </el-input>

    <el-dialog
      v-model="dialogVisible"
      title="选择路径"
      width="60%"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
    >
      <div class="path-browser">
        <!-- 当前路径 -->
        <div class="current-path">
          <el-breadcrumb separator="/">
            <el-breadcrumb-item
              v-for="(part, index) in pathParts"
              :key="index"
              @click="handleNavigate(index)"
            >
              {{ part || '根目录' }}
            </el-breadcrumb-item>
          </el-breadcrumb>
        </div>

        <!-- 文件列表 -->
        <el-table
          :data="fileList"
          style="width: 100%"
          height="400"
          @row-dblclick="handleRowDblclick"
        >
          <el-table-column prop="name" label="名称">
            <template #default="{ row }">
              <el-icon v-if="row.type === 'directory'"><Folder /></el-icon>
              <el-icon v-else><Document /></el-icon>
              <span class="ml-2">{{ row.name }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="type" label="类型" width="120">
            <template #default="{ row }">
              {{ row.type === 'directory' ? '文件夹' : '文件' }}
            </template>
          </el-table-column>
          <el-table-column prop="size" label="大小" width="120">
            <template #default="{ row }">
              {{ row.type === 'directory' ? '-' : formatSize(row.size) }}
            </template>
          </el-table-column>
          <el-table-column prop="modTime" label="修改时间" width="180">
            <template #default="{ row }">
              {{ formatTime(row.modTime) }}
            </template>
          </el-table-column>
        </el-table>

        <!-- 新建文件夹 -->
        <div v-if="createDir" class="create-dir">
          <el-input
            v-model="newDirName"
            placeholder="请输入文件夹名称"
            @keyup.enter="handleCreateDir"
          >
            <template #append>
              <el-button @click="handleCreateDir">创建</el-button>
            </template>
          </el-input>
        </div>
      </div>

      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleConfirm">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { Folder, Document } from '@element-plus/icons-vue'
import { request } from '@/utils/request'

interface FileInfo {
  name: string
  type: 'file' | 'directory'
  size: number
  modTime: string
}

const props = defineProps<{
  modelValue: string
  placeholder?: string
  rootPath?: string
  createDir?: boolean
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void
  (e: 'change', value: string): void
}>()

const dialogVisible = ref(false)
const currentPath = ref('')
const localValue = ref(props.modelValue)
const fileList = ref<FileInfo[]>([])
const newDirName = ref('')

// 监听 modelValue 变化
watch(() => props.modelValue, (val) => {
  localValue.value = val
  currentPath.value = val
})

// 计算路径部分
const pathParts = computed(() => {
  const path = currentPath.value || props.rootPath || '/'
  return path.split('/').filter(Boolean)
})

// 格式化文件大小
const formatSize = (size: number) => {
  if (size < 1024) return `${size} B`
  if (size < 1024 * 1024) return `${(size / 1024).toFixed(2)} KB`
  if (size < 1024 * 1024 * 1024) return `${(size / 1024 / 1024).toFixed(2)} MB`
  return `${(size / 1024 / 1024 / 1024).toFixed(2)} GB`
}

// 格式化时间
const formatTime = (time: string) => {
  return new Date(time).toLocaleString()
}

// 加载目录内容
const loadDirectory = async (path: string) => {
  try {
    const { data } = await request.get<FileInfo[]>('/api/file/list', {
      params: { path }
    })
    fileList.value = data
  } catch (error) {
    ElMessage.error('加载目录失败')
  }
}

// 处理路径导航
const handleNavigate = (index: number) => {
  const parts = pathParts.value
  currentPath.value = '/' + parts.slice(0, index + 1).join('/')
  loadDirectory(currentPath.value)
}

// 处理行双击
const handleRowDblclick = (row: FileInfo) => {
  if (row.type === 'directory') {
    currentPath.value = currentPath.value + '/' + row.name
    loadDirectory(currentPath.value)
  }
}

// 处理选择按钮点击
const handleSelect = () => {
  dialogVisible.value = true
  currentPath.value = localValue.value || props.rootPath || '/'
  loadDirectory(currentPath.value)
}

// 处理确认选择
const handleConfirm = () => {
  localValue.value = currentPath.value
  emit('update:modelValue', currentPath.value)
  emit('change', currentPath.value)
  dialogVisible.value = false
}

// 处理输入框变化
const handleChange = (value: string) => {
  localValue.value = value
  emit('update:modelValue', value)
  emit('change', value)
}

// 处理创建目录
const handleCreateDir = async () => {
  if (!newDirName.value) {
    ElMessage.warning('请输入文件夹名称')
    return
  }

  try {
    await request.post('/api/file/mkdir', {
      path: currentPath.value + '/' + newDirName.value
    })
    ElMessage.success('创建成功')
    newDirName.value = ''
    loadDirectory(currentPath.value)
  } catch (error) {
    ElMessage.error('创建失败')
  }
}
</script>

<style scoped>
.path-selector {
  width: 100%;
}

.path-browser {
  margin-bottom: 20px;
}

.current-path {
  margin-bottom: 16px;
  padding: 8px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.create-dir {
  margin-top: 16px;
}

:deep(.el-breadcrumb__item) {
  cursor: pointer;
}

.ml-2 {
  margin-left: 8px;
}
</style>

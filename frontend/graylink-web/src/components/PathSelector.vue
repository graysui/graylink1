<template>
  <div class="path-selector">
    <el-input
      v-model="localValue"
      :placeholder="placeholder"
      @change="handleChange"
    >
      <template #append>
        <el-button @click="handleSelect">
          选择
        </el-button>
      </template>
    </el-input>
    
    <!-- 路径选择对话框 -->
    <el-dialog
      v-model="dialogVisible"
      title="选择路径"
      width="500px"
    >
      <div class="path-browser">
        <!-- 当前路径显示 -->
        <div class="current-path">
          <el-breadcrumb separator="/">
            <el-breadcrumb-item 
              v-for="(part, index) in pathParts" 
              :key="index"
              @click="navigateTo(index)"
            >
              {{ part || '根目录' }}
            </el-breadcrumb-item>
          </el-breadcrumb>
        </div>

        <!-- 目录列表 -->
        <el-scrollbar height="300px">
          <el-table
            :data="dirList"
            style="width: 100%"
            @row-click="handleRowClick"
          >
            <el-table-column width="50">
              <template #default="{ row }">
                <el-icon><Folder /></el-icon>
              </template>
            </el-table-column>
            <el-table-column prop="name" label="名称" />
          </el-table>
        </el-scrollbar>

        <!-- 新建目录 -->
        <div v-if="createDir" class="create-dir">
          <el-input
            v-model="newDirName"
            placeholder="新目录名称"
            @keyup.enter="handleCreateDir"
          >
            <template #append>
              <el-button @click="handleCreateDir">
                创建
              </el-button>
            </template>
          </el-input>
        </div>
      </div>

      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleConfirm">
            确定
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { Folder } from '@element-plus/icons-vue'
import { settingApi } from '@/api/setting'
import type { DirListItem } from '@/api/setting'

const props = defineProps<{
  modelValue: string
  rootPath?: string
  placeholder?: string
  createDir?: boolean
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void
}>()

const dialogVisible = ref(false)
const currentPath = ref(props.modelValue || props.rootPath || '/')
const dirList = ref<{ name: string }[]>([])
const showNewDirDialog = ref(false)
const newDirName = ref('')
const localValue = ref(props.modelValue)

// 计算当前路径的各个部分
const pathParts = computed(() => {
  return currentPath.value.split('/').filter(Boolean)
})

// 导航到指定层级
const navigateTo = async (index: number) => {
  const newPath = '/' + pathParts.value.slice(0, index + 1).join('/')
  await loadDirList(newPath)
}

// 加载目录列表
const loadDirList = async (path: string) => {
  try {
    const { data } = await settingApi.listDir(path)
    dirList.value = data.map(item => ({ name: item.name }))
  } catch (error) {
    ElMessage.error('加载目录失败')
  }
}

// 处理行点击
const handleRowClick = async (row: { name: string }) => {
  const newPath = currentPath.value + '/' + row.name
  await loadDirList(newPath)
}

// 处理选择按钮点击
const handleSelect = async () => {
  dialogVisible.value = true
  currentPath.value = props.rootPath || '/'
  await loadDirList(currentPath.value)
}

// 处理创建目录
const handleCreateDir = async () => {
  if (!newDirName.value) {
    ElMessage.warning('请输入目录名称')
    return
  }

  try {
    await settingApi.createDir(currentPath.value + '/' + newDirName.value)
    await loadDirList(currentPath.value)
    newDirName.value = ''
    ElMessage.success('创建成功')
  } catch (error) {
    ElMessage.error('创建目录失败')
  }
}

// 处理确认选择
const handleConfirm = () => {
  localValue.value = currentPath.value
  emit('update:modelValue', currentPath.value)
  dialogVisible.value = false
}

// 处理输入框变化
const handleChange = (value: string) => {
  emit('update:modelValue', value)
}

// 监听 modelValue 变化
watch(() => props.modelValue, (newValue) => {
  localValue.value = newValue
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
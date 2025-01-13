<template>
  <div class="path-selector">
    <el-input
      v-model="currentPath"
      placeholder="请输入路径"
      clearable
      @change="handlePathChange"
    >
      <template #append>
        <el-button @click="showDialog = true">
          <el-icon><Folder /></el-icon>
        </el-button>
      </template>
    </el-input>

    <!-- 路径选择对话框 -->
    <el-dialog
      v-model="showDialog"
      title="选择路径"
      width="500px"
    >
      <el-tree
        ref="treeRef"
        :data="treeData"
        :props="treeProps"
        :load="loadNode"
        lazy
        node-key="path"
        @node-click="handleNodeClick"
      />
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showDialog = false">取消</el-button>
          <el-button type="primary" @click="confirmSelection">
            确定
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { Folder } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import type { TreeInstance } from 'element-plus'

const props = defineProps<{
  modelValue: string
  rootPath?: string
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void
  (e: 'change', value: string): void
}>()

const currentPath = ref(props.modelValue || '/')
const showDialog = ref(false)
const selectedPath = ref('')
const treeRef = ref<TreeInstance>()

// 树形控件配置
const treeProps = {
  label: 'name',
  children: 'children',
  isLeaf: 'isLeaf'
}

const treeData = ref([
  { name: '/', path: '/', isLeaf: false }
])

// 监听值变化
watch(() => props.modelValue, (newValue) => {
  currentPath.value = newValue
})

// 路径变更处理
const handlePathChange = async (path: string) => {
  const normalizedPath = path.startsWith('/') ? path : `/${path}`
  currentPath.value = normalizedPath
  emit('update:modelValue', normalizedPath)
  emit('change', normalizedPath)
}

// 加载节点数据
const loadNode = async (node: any, resolve: (data: any[]) => void) => {
  try {
    if (node.level === 0) {
      resolve([{ name: '/', path: '/' }])
      return
    }

    const path = node.data.path
    const response = await fetch(`/api/file/list?path=${encodeURIComponent(path)}`)
    const { data } = await response.json()

    const children = data
      .filter((item: any) => item.is_directory)
      .map((item: any) => ({
        name: item.name,
        path: item.path,
        isLeaf: false
      }))

    resolve(children)
  } catch (error) {
    console.error('加载目录失败:', error)
    ElMessage.error('加载目录失败')
    resolve([])
  }
}

// 处理节点点击
const handleNodeClick = (data: any) => {
  selectedPath.value = data.path
}

// 确认选择
const confirmSelection = () => {
  if (selectedPath.value) {
    handlePathChange(selectedPath.value)
    showDialog.value = false
  }
}
</script>

<style scoped>
.path-selector {
  width: 100%;
}

.dialog-footer {
  padding-top: 20px;
  text-align: right;
}
</style> 
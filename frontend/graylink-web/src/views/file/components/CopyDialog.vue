<template>
  <el-dialog
    v-model="dialogVisible"
    title="复制到"
    width="500px"
  >
    <el-tree
      ref="treeRef"
      :data="treeData"
      :props="defaultProps"
      @node-click="handleNodeClick"
    />
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleConfirm">
          确认
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import type { FileInfo } from '@/types/api'
import type { FileItem } from '@/types/file'
import { useFileStore } from '@/stores/modules/file'

const props = defineProps<{
  modelValue: boolean
  files: FileInfo[]
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: boolean): void
  (e: 'success'): void
}>()

const fileStore = useFileStore()
const treeRef = ref()
const selectedPath = ref('')

const dialogVisible = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

interface TreeNode extends FileItem {
  children?: TreeNode[]
}

const treeData = ref<TreeNode[]>([])
const defaultProps = {
  children: 'children',
  label: 'name'
}

// 获取目录树数据
const loadDirectoryTree = async () => {
  try {
    const response = await fileStore.loadDirectoryTree()
    treeData.value = [{
      name: '根目录',
      path: '/',
      type: 'directory',
      children: response
    }]
  } catch (error) {
    ElMessage.error('加载目录结构失败')
  }
}

// 组件挂载时加载目录树
onMounted(() => {
  loadDirectoryTree()
})

const handleNodeClick = (data: any) => {
  selectedPath.value = data.path
}

const handleConfirm = async () => {
  if (!selectedPath.value) {
    ElMessage.warning('请选择目标目录')
    return
  }

  try {
    const paths = props.files.map(file => file.path)
    await fileStore.batchOperation('copy', paths, selectedPath.value)
    ElMessage.success('复制成功')
    dialogVisible.value = false
    emit('success')
  } catch (error) {
    ElMessage.error('复制失败')
  }
}
</script>

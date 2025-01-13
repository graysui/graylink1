<template>
  <div class="file-page">
    <div class="toolbar">
      <el-breadcrumb>
        <el-breadcrumb-item
          v-for="item in pathItems"
          :key="item.path"
          :to="{ path: item.path }"
        >
          {{ item.name }}
        </el-breadcrumb-item>
      </el-breadcrumb>

      <div class="actions">
        <el-button-group>
          <el-button
            :icon="Refresh"
            @click="refreshList"
            :loading="loading"
          >
            刷新
          </el-button>
          <el-button
            :icon="Upload"
            @click="showUploadDialog"
          >
            上传
          </el-button>
        </el-button-group>
      </div>
    </div>

    <el-table
      ref="tableRef"
      v-loading="loading"
      :data="fileList"
      style="width: 100%"
      @sort-change="handleSortChange"
      @selection-change="handleSelectionChange"
    >
      <el-table-column type="selection" width="55" />

      <el-table-column
        prop="name"
        label="名称"
        sortable="custom"
      >
        <template #default="{ row }">
          <div class="file-name">
            <el-icon>
              <component :is="getFileIcon(row)" />
            </el-icon>
            <span
              class="name"
              @click="handleFileClick(row)"
            >
              {{ row.name }}
            </span>
          </div>
        </template>
      </el-table-column>

      <el-table-column
        prop="size"
        label="大小"
        width="120"
        sortable="custom"
      >
        <template #default="{ row }">
          {{ formatFileSize(row.size) }}
        </template>
      </el-table-column>

      <el-table-column
        prop="modified_time"
        label="修改时间"
        width="180"
        sortable="custom"
      >
        <template #default="{ row }">
          {{ formatTime(row.modified_time) }}
        </template>
      </el-table-column>

      <el-table-column
        label="操作"
        width="150"
        fixed="right"
      >
        <template #default="{ row }">
          <el-button-group>
            <el-button
              link
              type="primary"
              :icon="Download"
              @click="downloadFile(row)"
            >
              下载
            </el-button>
            <el-dropdown trigger="click">
              <el-button link type="primary" :icon="More">
                更多
              </el-button>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item @click="showMoveDialog(row)">
                    移动
                  </el-dropdown-item>
                  <el-dropdown-item @click="showCopyDialog(row)">
                    复制
                  </el-dropdown-item>
                  <el-dropdown-item
                    divided
                    @click="confirmDelete(row)"
                  >
                    删除
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </el-button-group>
        </template>
      </el-table-column>
    </el-table>

    <!-- 批量操作工具栏 -->
    <div
      v-show="selectedFiles.length"
      class="batch-toolbar"
    >
      <span class="info">
        已选择 {{ selectedFiles.length }} 个文件
      </span>
      <el-button-group>
        <el-button
          type="primary"
          :icon="FolderAdd"
          @click="showBatchMoveDialog"
        >
          批量移动
        </el-button>
        <el-button
          type="primary"
          :icon="CopyIcon"
          @click="showBatchCopyDialog"
        >
          批量复制
        </el-button>
        <el-button
          type="danger"
          :icon="Delete"
          @click="confirmBatchDelete"
        >
          批量删除
        </el-button>
      </el-button-group>
    </div>

    <!-- 各种对话框组件 -->
    <file-preview
      v-if="currentFile"
      :file-info="currentFile"
      :visible="previewVisible"
      @update:visible="previewVisible = $event"
    />

    <upload-dialog
      v-model="uploadVisible"
      :current-path="currentPath"
      @success="refreshList"
    />

    <move-dialog
      v-model="moveVisible"
      :files="selectedFiles"
      @success="handleOperationSuccess"
    />

    <copy-dialog
      v-model="copyVisible"
      :files="selectedFiles"
      @success="handleOperationSuccess"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import {
  Refresh,
  Upload,
  Download,
  More,
  FolderAdd,
  Document as DocumentIcon,
  Delete,
  Link,
  Picture,
  VideoCamera,
  Headset
} from '@element-plus/icons-vue'
import { ElMessageBox, ElMessage } from 'element-plus'
import { useFileStore } from '@/stores/modules/file'
import { formatFileSize, formatTime } from '@/utils/format'
import type { FileInfo } from '@/types/api'
import FilePreview from '@/components/common/FilePreview.vue'
import UploadDialog from './components/UploadDialog.vue'
import MoveDialog from './components/MoveDialog.vue'
import CopyDialog from './components/CopyDialog.vue'

const route = useRoute()
const router = useRouter()
const fileStore = useFileStore()

// 状态
const loading = ref(false)
const currentFile = ref<FileInfo | null>(null)
const selectedFiles = ref<FileInfo[]>([])
const previewVisible = ref(false)
const uploadVisible = ref(false)
const moveVisible = ref(false)
const copyVisible = ref(false)

// 计算属性
const currentPath = computed(() => route.query.path as string || '/')
const pathItems = computed(() => {
  const paths = currentPath.value.split('/').filter(Boolean)
  return [
    { name: '根目录', path: '/' },
    ...paths.map((name, index) => ({
      name,
      path: '/' + paths.slice(0, index + 1).join('/')
    }))
  ]
})

const fileList = computed(() => {
  return fileStore.files
})

// 方法
const refreshList = async () => {
  try {
    loading.value = true
    await fileStore.loadFiles(currentPath.value)
  } catch (error) {
    ElMessage.error('加载文件列表失败')
  } finally {
    loading.value = false
  }
}

const handleFileClick = (file: FileInfo) => {
  if (file.is_directory) {
    router.push({
      query: { path: file.path }
    })
  } else {
    currentFile.value = file
    previewVisible.value = true
  }
}

const handleSortChange = ({ prop, order }: any) => {
  if (prop) {
    fileStore.setSorting(prop, order === 'descending')
  }
}

const handleSelectionChange = (files: FileInfo[]) => {
  selectedFiles.value = files
}

const handleOperationSuccess = () => {
  selectedFiles.value = []
  refreshList()
}

const confirmDelete = async (file: FileInfo) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除 ${file.name} 吗？`,
      '删除确认',
      {
        type: 'warning'
      }
    )
    await fileStore.batchOperation('delete', [file.path])
    ElMessage.success('删除成功')
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const confirmBatchDelete = async () => {
  try {
    await ElMessageBox.confirm(
      `确定要删除选中的 ${selectedFiles.value.length} 个文件吗？`,
      '批量删除确认',
      {
        type: 'warning'
      }
    )
    const paths = selectedFiles.value.map(file => file.path)
    await fileStore.batchOperation('delete', paths)
    ElMessage.success('批量删除成功')
    handleOperationSuccess()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('批量删除失败')
    }
  }
}

const showUploadDialog = () => {
  uploadVisible.value = true
}

const showMoveDialog = (file: FileInfo) => {
  selectedFiles.value = [file]
  moveVisible.value = true
}

const showCopyDialog = (file: FileInfo) => {
  selectedFiles.value = [file]
  copyVisible.value = true
}

const showBatchMoveDialog = () => {
  moveVisible.value = true
}

const showBatchCopyDialog = () => {
  copyVisible.value = true
}

const getFileIcon = (file: FileInfo) => {
  if (file.is_directory) return FolderAdd
  switch (file.type) {
    case 'image': return Picture
    case 'video': return VideoCamera
    case 'audio': return Headset
    case 'document': return DocumentIcon
    default: return DocumentIcon
  }
}

const downloadFile = async (file: FileInfo) => {
  try {
    // 实现下载逻辑
  } catch (error) {
    console.error('下载失败:', error)
  }
}

// 生命周期
onMounted(() => {
  refreshList()
})

onBeforeUnmount(() => {
  selectedFiles.value = []
})

// 重命名避免冲突
const CopyIcon = DocumentIcon
const FolderFilledIcon = FolderAdd

const loadFiles = async (path: string) => {
  await fileStore.getSnapshot(path)
}

const setSorting = (prop: string, order: string) => {
  fileStore.setSorting(prop, order === 'descending')
}

const batchOperation = async (operation: string, paths: string[]) => {
  await fileStore.batchOperation(operation, paths)
}
</script>

<style scoped lang="scss">
.file-page {
  .toolbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
  }

  .file-name {
    display: flex;
    align-items: center;
    gap: 8px;

    .name {
      cursor: pointer;

      &:hover {
        color: var(--el-color-primary);
      }
    }
  }

  .batch-toolbar {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    padding: 12px 24px;
    background-color: #fff;
    box-shadow: 0 -2px 8px rgba(0, 0, 0, 0.15);
    display: flex;
    justify-content: space-between;
    align-items: center;
    z-index: 100;

    .info {
      color: #666;
    }
  }
}
</style>

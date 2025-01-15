import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { FileRecord, ApiResponse, PaginatedResponse } from '@/types/api'
import { request } from '@/utils/request'

interface DirectoryTree {
  tree: any[]
}

interface FileOperations {
  operation: 'move' | 'copy' | 'delete'
  paths: string[]
  targetPath?: string
}

export const useFileStore = defineStore('file', () => {
  const currentPath = ref('')
  const files = ref<FileRecord[]>([])
  const selectedFiles = ref<string[]>([])
  const sortBy = ref('name')
  const sortDesc = ref(false)
  const loading = ref(false)

  async function loadFiles(path: string) {
    loading.value = true
    try {
      const response = await request.get<PaginatedResponse<FileRecord>>(`/api/files?path=${encodeURIComponent(path)}`)
      files.value = response.data.data.items
      currentPath.value = path
    } finally {
      loading.value = false
    }
  }

  async function loadDirectoryTree() {
    try {
      const response = await request.get<ApiResponse<DirectoryTree>>('/api/files/tree')
      return response.data.data.tree
    } catch (error) {
      console.error('Failed to load directory tree:', error)
      return []
    }
  }

  function setSorting(by: string, desc: boolean) {
    sortBy.value = by
    sortDesc.value = desc
    files.value.sort((a, b) => {
      const aValue = a[by as keyof FileRecord]
      const bValue = b[by as keyof FileRecord]

      if (aValue === undefined && bValue === undefined) return 0
      if (aValue === undefined) return desc ? 1 : -1
      if (bValue === undefined) return desc ? -1 : 1

      return desc
        ? String(bValue).localeCompare(String(aValue))
        : String(aValue).localeCompare(String(bValue))
    })
  }

  async function batchOperation(operation: FileOperations) {
    loading.value = true
    try {
      await request.post<ApiResponse<void>>('/api/files/batch', operation)
      await loadFiles(currentPath.value)
    } finally {
      loading.value = false
    }
  }

  return {
    currentPath,
    files,
    selectedFiles,
    sortBy,
    sortDesc,
    loading,
    loadFiles,
    setSorting,
    batchOperation,
    loadDirectoryTree
  }
})

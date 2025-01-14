import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { FileItem, FileOperations } from '@/types/file'
import { fileApi } from '@/api/file'

export const useFileStore = defineStore('file', () => {
  const currentPath = ref('')
  const files = ref<FileItem[]>([])
  const selectedFiles = ref<string[]>([])
  const sortBy = ref('name')
  const sortDesc = ref(false)
  const loading = ref(false)

  async function loadFiles(path: string) {
    loading.value = true
    try {
      const response = await fileApi.getFiles(path)
      files.value = response.data.items
      currentPath.value = path
    } finally {
      loading.value = false
    }
  }

  async function loadDirectoryTree() {
    try {
      const response = await fileApi.getDirectoryTree()
      return response.data.tree
    } catch (error) {
      console.error('Failed to load directory tree:', error)
      return []
    }
  }

  function setSorting(by: string, desc: boolean) {
    sortBy.value = by
    sortDesc.value = desc
    files.value.sort((a, b) => {
      const aValue = a[by as keyof FileItem]
      const bValue = b[by as keyof FileItem]

      if (aValue === undefined && bValue === undefined) return 0
      if (aValue === undefined) return desc ? 1 : -1
      if (bValue === undefined) return desc ? -1 : 1

      return desc
        ? String(bValue).localeCompare(String(aValue))
        : String(aValue).localeCompare(String(bValue))
    })
  }

  async function batchOperation(operation: FileOperations, paths: string[], targetPath?: string) {
    loading.value = true
    try {
      await fileApi.batchOperation({ operation, paths, targetPath })
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

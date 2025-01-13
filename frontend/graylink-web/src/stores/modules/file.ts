import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { fileApi } from '@/api'
import type { FileInfo, DatabaseStats } from '@/types/api'
import { useRoute } from 'vue-router'

export const useFileStore = defineStore('file', () => {
  const route = useRoute()
  const currentPath = computed(() => route.query.path as string || '/')
  const files = ref<FileInfo[]>([])
  const stats = ref<DatabaseStats | null>(null)
  const loading = ref(false)

  async function loadFiles(path: string) {
    try {
      loading.value = true
      files.value = await fileApi.getSnapshot(path)
      return files.value
    } finally {
      loading.value = false
    }
  }

  async function batchOperation(operation: 'delete' | 'move' | 'copy', paths: string[], target?: string) {
    try {
      loading.value = true
      if (operation === 'move' || operation === 'copy') {
        if (!target) throw new Error('Target path is required for move/copy operations')
        await fileApi[operation](paths, target)
      } else {
        await fileApi[operation](paths)
      }
      await loadFiles(currentPath.value)
    } finally {
      loading.value = false
    }
  }

  function setSorting(prop: keyof FileInfo, isDesc: boolean) {
    const sorted = [...files.value].sort((a, b) => {
      const aValue = a[prop]
      const bValue = b[prop]
      if (aValue === undefined || bValue === undefined) return 0
      return isDesc ? 
        (String(bValue) > String(aValue) ? 1 : -1) : 
        (String(aValue) > String(bValue) ? 1 : -1)
    })
    files.value = sorted
  }

  async function getStats() {
    try {
      loading.value = true
      stats.value = await fileApi.getStats()
      return stats.value
    } finally {
      loading.value = false
    }
  }

  async function cleanupDatabase() {
    try {
      loading.value = true
      await fileApi.cleanup()
      await getStats()
    } finally {
      loading.value = false
    }
  }

  const getFiles = async () => {
    try {
      loading.value = true
      files.value = await fileApi.getSnapshot()
    } catch (error) {
      console.error('获取文件列表失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  return {
    files,
    stats,
    loading,
    currentPath,
    loadFiles,
    batchOperation,
    setSorting,
    getStats,
    cleanupDatabase,
    getFiles
  }
}) 
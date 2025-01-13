import { defineStore } from 'pinia'
import { ref } from 'vue'
import { embyApi } from '@/api'
import type { EmbyLibrary, EmbyStatus } from '@/types/api'

export const useEmbyStore = defineStore('emby', () => {
  // 状态
  const libraries = ref<EmbyLibrary[]>([])
  const loading = ref(false)
  const status = ref<EmbyStatus>({
    serverStatus: 'disconnected',
    apiStatus: false
  })
  const refreshProgress = ref<Record<string, number>>({})

  // actions
  const checkStatus = async () => {
    try {
      loading.value = true
      const result = await embyApi.checkStatus()
      status.value = result
      return result
    } catch (error) {
      console.error('检查服务器状态失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  const getLibraries = async () => {
    try {
      loading.value = true
      const libraryList = await embyApi.getLibraries()
      libraries.value = libraryList
      return libraryList
    } catch (error) {
      console.error('获取媒体库列表失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  const refreshByPaths = async (paths: string[], libraryId: string) => {
    try {
      loading.value = true
      updateRefreshProgress(libraryId, 0)

      // 模拟进度更新
      const progressInterval = setInterval(() => {
        const currentProgress = refreshProgress.value[libraryId] || 0
        if (currentProgress < 90) {
          updateRefreshProgress(libraryId, currentProgress + 10)
        }
      }, 1000)

      await embyApi.refreshByPaths(paths)
      
      clearInterval(progressInterval)
      updateRefreshProgress(libraryId, 100)
      setTimeout(() => clearRefreshProgress(libraryId), 2000)
    } catch (error) {
      console.error('刷新媒体库失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  const refreshRoot = async () => {
    try {
      loading.value = true
      await embyApi.refreshRoot()
    } catch (error) {
      console.error('刷新根媒体库失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  const updateRefreshProgress = (libraryId: string, progress: number) => {
    refreshProgress.value[libraryId] = progress
  }

  const clearRefreshProgress = (libraryId: string) => {
    delete refreshProgress.value[libraryId]
  }

  return {
    libraries,
    loading,
    status,
    checkStatus,
    getLibraries,
    refreshByPaths,
    refreshRoot,
    refreshProgress,
    updateRefreshProgress,
    clearRefreshProgress
  }
}) 
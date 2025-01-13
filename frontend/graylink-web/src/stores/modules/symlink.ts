import { defineStore } from 'pinia'
import { ref } from 'vue'
import { symlinkApi } from '@/api'
import type { VerifyResult } from '@/types/api'

export const useSymlinkStore = defineStore('symlink', () => {
  const verifyResult = ref<VerifyResult | null>(null)
  const loading = ref(false)

  async function verifySymlinks() {
    try {
      loading.value = true
      const response = await symlinkApi.verify()
      verifyResult.value = {
        broken_links: response.data.broken_links || [],
        invalid_targets: response.data.invalid_targets || [],
        timestamp: new Date().toISOString(),
        stats: {
          total: (response.data.broken_links?.length || 0) + (response.data.invalid_targets?.length || 0),
          broken: response.data.broken_links?.length || 0,
          invalid: response.data.invalid_targets?.length || 0
        }
      }
    } finally {
      loading.value = false
    }
  }

  const createSymlink = async (relativePath: string) => {
    try {
      loading.value = true
      return await symlinkApi.create(relativePath)
    } catch (error) {
      console.error('创建软链接失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  const removeSymlink = async (relativePath: string) => {
    try {
      loading.value = true
      return await symlinkApi.remove(relativePath)
    } catch (error) {
      console.error('删除软链接失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  const rebuildSymlinks = async () => {
    try {
      loading.value = true
      return await symlinkApi.rebuild()
    } catch (error) {
      console.error('重建软链接失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  const clearSymlinks = async () => {
    try {
      loading.value = true
      return await symlinkApi.clear()
    } catch (error) {
      console.error('清理软链接失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  return {
    verifyResult,
    loading,
    verifySymlinks,
    createSymlink,
    removeSymlink,
    rebuildSymlinks,
    clearSymlinks
  }
}) 
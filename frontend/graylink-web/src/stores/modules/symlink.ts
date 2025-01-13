import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { SymlinkState } from '../types'

export const useSymlinkStore = defineStore('symlink', () => {
  const symlinks = ref<SymlinkState['symlinks']['value']>([])
  const verifying = ref(false)

  const verifySymlinks = async () => {
    verifying.value = true
    try {
      const response = await api.get('/symlinks/verify')
      symlinks.value = response.data
    } finally {
      verifying.value = false
    }
  }

  return {
    symlinks,
    verifying,
    verifySymlinks
  }
})

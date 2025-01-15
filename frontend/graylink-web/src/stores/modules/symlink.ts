import { defineStore } from 'pinia'
import { request } from '@/utils/request'
import type { ApiResponse, SymlinkState } from '@/types/api'

interface State {
  symlinks: {
    value: any[]
  }
  verifying: boolean
  verifyResult: SymlinkState
  loading: boolean
}

export const useSymlinkStore = defineStore('symlink', {
  state: (): State => ({
    symlinks: {
      value: []
    },
    verifying: false,
    verifyResult: {
      total: 0,
      valid: 0,
      invalid: 0,
      missing: 0
    },
    loading: false
  }),

  actions: {
    async verifySymlinks() {
      this.verifying = true
      try {
        const response = await request.get<ApiResponse<SymlinkState>>('/api/symlink/verify')
        this.verifyResult = response.data.data
      } finally {
        this.verifying = false
      }
    },

    async createSymlink(data: { source: string; target: string }) {
      this.loading = true
      try {
        await request.post<ApiResponse<void>>('/api/symlink', data)
        await this.verifySymlinks()
      } finally {
        this.loading = false
      }
    },

    async removeSymlink(path: string) {
      this.loading = true
      try {
        await request.delete<ApiResponse<void>>(`/api/symlink/${encodeURIComponent(path)}`)
        await this.verifySymlinks()
      } finally {
        this.loading = false
      }
    },

    async clearSymlinks() {
      this.loading = true
      try {
        await request.delete<ApiResponse<void>>('/api/symlink')
        await this.verifySymlinks()
      } finally {
        this.loading = false
      }
    },

    async rebuildSymlinks() {
      this.loading = true
      try {
        const response = await request.post<ApiResponse<SymlinkState>>('/api/symlink/rebuild')
        return response.data.data
      } finally {
        this.loading = false
      }
    }
  }
})

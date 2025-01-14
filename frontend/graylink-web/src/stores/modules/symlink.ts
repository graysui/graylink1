import { defineStore } from 'pinia'
import { api } from '@/utils/request'
import type { VerifyResult, SymlinkState } from '@/types/symlink'
import type { ApiResponse } from '@/types/response'

export const useSymlinkStore = defineStore('symlink', {
  state: (): SymlinkState => ({
    symlinks: {
      value: []
    },
    verifying: false,
    verifyResult: {
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
        const response = await api.get<ApiResponse<VerifyResult>>('/api/symlinks/verify')
        this.verifyResult = response.data.data
      } finally {
        this.verifying = false
      }
    },

    async createSymlink(data: { source: string; target: string }) {
      this.loading = true
      try {
        await api.post<ApiResponse<void>>('/api/symlinks', { path: data.source })
        await this.verifySymlinks()
      } finally {
        this.loading = false
      }
    },

    async removeSymlink(path: string) {
      this.loading = true
      try {
        await api.delete<ApiResponse<void>>(`/api/symlinks/${encodeURIComponent(path)}`)
        await this.verifySymlinks()
      } finally {
        this.loading = false
      }
    },

    async clearSymlinks() {
      this.loading = true
      try {
        await api.delete<ApiResponse<void>>('/api/symlinks')
        await this.verifySymlinks()
      } finally {
        this.loading = false
      }
    },

    async rebuildSymlinks() {
      this.loading = true
      try {
        const response = await api.post<ApiResponse<VerifyResult>>('/api/symlinks/rebuild')
        return response.data.data
      } finally {
        this.loading = false
      }
    }
  }
})

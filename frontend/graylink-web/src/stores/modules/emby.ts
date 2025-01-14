import { defineStore } from 'pinia'
import { api } from '@/utils/request'
import type { EmbyState, EmbyStatus, EmbyLibrary } from '@/types/emby'
import type { ApiResponse } from '@/types/response'

export const useEmbyStore = defineStore('emby', {
  state: (): EmbyState => ({
    status: {
      serverStatus: 'disconnected',
      apiStatus: false,
      version: undefined,
      lastCheck: undefined,
      lastUpdate: undefined
    },
    libraries: [],
    refreshProgress: {}
  }),

  actions: {
    async checkStatus() {
      try {
        const response = await api.get<ApiResponse<EmbyStatus>>('/api/emby/status')
        this.status = response.data.data
      } catch (error) {
        this.status.serverStatus = 'disconnected'
        this.status.apiStatus = false
        throw error
      }
    },

    async getLibraries() {
      try {
        const response = await api.get<ApiResponse<EmbyLibrary[]>>('/api/emby/libraries')
        this.libraries = response.data.data
      } catch (error) {
        this.libraries = []
        throw error
      }
    },

    async refreshByPaths(paths: string[]) {
      await api.post<ApiResponse<void>>('/api/emby/refresh', { paths })
    },

    async refreshRoot() {
      await api.post<ApiResponse<void>>('/api/emby/refresh')
    },

    updateRefreshProgress(libraryId: string, progress: number) {
      this.refreshProgress[libraryId] = progress
    }
  }
})

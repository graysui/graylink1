import { defineStore } from 'pinia'
import { request } from '@/utils/request'
import type { ApiResponse, EmbyStatus } from '@/types/api'

interface EmbyLibrary {
  id: string
  name: string
  path: string
}

interface State {
  status: EmbyStatus
  libraries: EmbyLibrary[]
  refreshProgress: Record<string, number>
}

export const useEmbyStore = defineStore('emby', {
  state: (): State => ({
    status: {
      connected: false,
      version: null,
      server_name: null
    },
    libraries: [],
    refreshProgress: {}
  }),

  actions: {
    async checkStatus() {
      try {
        const response = await request.get<ApiResponse<EmbyStatus>>('/api/emby/status')
        this.status = response.data.data
      } catch (error) {
        this.status.connected = false
        throw error
      }
    },

    async getLibraries() {
      try {
        const response = await request.get<ApiResponse<EmbyLibrary[]>>('/api/emby/libraries')
        this.libraries = response.data.data
      } catch (error) {
        this.libraries = []
        throw error
      }
    },

    async refreshByPaths(paths: string[]) {
      await request.post<ApiResponse<void>>('/api/emby/refresh', { paths })
    },

    async refreshRoot() {
      await request.post<ApiResponse<void>>('/api/emby/refresh/root')
    },

    updateRefreshProgress(libraryId: string, progress: number) {
      this.refreshProgress[libraryId] = progress
    }
  }
})

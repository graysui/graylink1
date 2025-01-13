import { defineStore } from 'pinia'
import { api } from '@/api'
import type { ApiResponse } from '@/api'

interface EmbyState {
  status: {
    connected: boolean
    version: string
    error?: string
  }
  libraries: Array<{
    id: string
    name: string
    path: string
    type: string
  }>
  loading: boolean
}

export const useEmbyStore = defineStore('emby', {
  state: (): EmbyState => ({
    status: {
      connected: false,
      version: '',
      error: undefined,
    },
    libraries: [],
    loading: false,
  }),

  actions: {
    async checkStatus() {
      this.loading = true
      try {
        const response = await api.get<ApiResponse<EmbyState['status']>>('/emby/status')
        this.status = response.data
      } finally {
        this.loading = false
      }
    },

    async getLibraries() {
      this.loading = true
      try {
        const response = await api.get<ApiResponse<EmbyState['libraries']>>('/emby/libraries')
        this.libraries = response.data
      } finally {
        this.loading = false
      }
    },

    async refreshByPaths(paths: string[]) {
      this.loading = true
      try {
        await api.post('/emby/refresh', { paths })
      } finally {
        this.loading = false
      }
    },

    async refreshRoot() {
      this.loading = true
      try {
        await api.post('/emby/refresh')
      } finally {
        this.loading = false
      }
    },
  },
})

import { defineStore } from 'pinia'
import { api } from '@/api'
import type { ApiResponse } from '@/api'

interface FileInfo {
  name: string
  path: string
  size: number
  type: 'file' | 'directory'
  modified: string
  children?: FileInfo[]
}

interface FileStats {
  total_size: number
  file_count: number
  dir_count: number
  last_scan: string
}

interface FileState {
  files: FileInfo[]
  stats: FileStats | null
  loading: boolean
  currentPath: string
}

export const useFileStore = defineStore('file', {
  state: (): FileState => ({
    files: [],
    stats: null,
    loading: false,
    currentPath: '/',
  }),

  actions: {
    async getSnapshot(path = '/') {
      this.loading = true
      try {
        const response = await api.get<ApiResponse<FileInfo[]>>('/files', {
          params: { path },
        })
        this.files = response.data
        this.currentPath = path
      } finally {
        this.loading = false
      }
    },

    async moveFiles(paths: string[], target: string) {
      this.loading = true
      try {
        await api.post('/files/move', {
          paths,
          target,
        })
        await this.getSnapshot(this.currentPath)
      } finally {
        this.loading = false
      }
    },

    async copyFiles(paths: string[], target: string) {
      this.loading = true
      try {
        await api.post('/files/copy', {
          paths,
          target,
        })
        await this.getSnapshot(this.currentPath)
      } finally {
        this.loading = false
      }
    },

    async deleteFiles(paths: string[]) {
      this.loading = true
      try {
        await api.post('/files/delete', { paths })
        await this.getSnapshot(this.currentPath)
      } finally {
        this.loading = false
      }
    },

    async getStats() {
      this.loading = true
      try {
        const response = await api.get<ApiResponse<FileStats>>('/files/stats')
        this.stats = response.data
      } finally {
        this.loading = false
      }
    },

    async cleanup() {
      this.loading = true
      try {
        await api.post('/files/cleanup')
        await this.getStats()
      } finally {
        this.loading = false
      }
    },
  },
})

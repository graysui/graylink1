import type { FileItem, FileOperations, FileApiResponse, BatchOperationParams } from '@/types/file'
import type { ApiResponse } from '@/types/api'
import { request } from '@/utils/request'

export const fileApi = {
  // 获取文件列表
  getFiles(path: string): Promise<ApiResponse<FileApiResponse>> {
    return request.get('/api/file/list', { params: { path } })
  },

  // 获取文件快照
  getSnapshot(path: string): Promise<ApiResponse<FileItem[]>> {
    return request.get('/api/monitor/snapshot', { params: { path } })
  },

  // 批量操作
  batchOperation(params: BatchOperationParams): Promise<ApiResponse<void>> {
    return request.post('/api/file/batch', params)
  },

  // 获取文件统计信息
  getStats(): Promise<ApiResponse<{ total: number, size: number }>> {
    return request.get('/api/file/stats')
  },

  // 获取目录树结构
  getDirectoryTree(): Promise<ApiResponse<{ tree: FileItem[] }>> {
    return request.get('/api/file/tree')
  }
}

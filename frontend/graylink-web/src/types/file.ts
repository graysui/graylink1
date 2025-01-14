export interface FileItem {
  name: string
  path: string
  type: 'file' | 'directory'
  size?: number
  modified?: string
  extension?: string
}

export type FileOperations = 'copy' | 'move' | 'delete'

export interface FileState {
  currentPath: string
  files: FileItem[]
  selectedFiles: string[]
  sortBy: string
  sortDesc: boolean
  loading: boolean
}

export interface FileInfo extends FileItem {
  id: string
  parent_id?: string
  created_at: string
  updated_at: string
}

export interface BatchOperationParams {
  operation: FileOperations
  paths: string[]
  targetPath?: string
}

export interface FileApiResponse {
  items: FileItem[]
  total: number
  path: string
}

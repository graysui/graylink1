import type { SystemSettings } from './settings'
import type { EmbyLibrary, EmbyStatus, EmbyState } from './emby'
import type { FileItem } from './settings'
import type { VerifyResult } from './symlink'

export interface SettingState {
  settings: SystemSettings
  loading: boolean
}

export interface FileState {
  currentPath: string
  files: FileItem[]
  sorting: {
    prop: string
    order: 'ascending' | 'descending'
  }
}

export interface SymlinkState {
  verifyResult: VerifyResult
  progress: {
    current: number
    total: number
    message?: string
  }
}

// Store方法类型
export interface SettingStore {
  getSettings(): Promise<void>
  saveSettings(settings: SystemSettings): Promise<void>
  updatePassword(oldPassword: string, newPassword: string): Promise<void>
  testEmbyConnection(config: SystemSettings['emby']): Promise<void>
}

export interface EmbyStore {
  checkStatus(): Promise<void>
  getLibraries(): Promise<void>
  refreshByPaths(paths: string[]): Promise<void>
  refreshRoot(): Promise<void>
  updateRefreshProgress(libraryId: string, progress: number): void
}

export interface FileStore {
  getSnapshot(path?: string): Promise<void>
  moveFiles(paths: string[], target: string): Promise<void>
  copyFiles(paths: string[], target: string): Promise<void>
  deleteFiles(paths: string[]): Promise<void>
  getStats(): Promise<void>
  cleanup(): Promise<void>
  loadFiles(path: string): Promise<void>
  setSorting(prop: string, descending: boolean): void
  batchOperation(operation: string, paths: string[]): Promise<void>
}

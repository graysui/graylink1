import type { SystemSettings } from './settings'
import type { EmbyLibrary, EmbyStatus } from './settings'

export interface SettingState {
  settings: SystemSettings
}

export interface EmbyState {
  libraries: EmbyLibrary[]
  status: EmbyStatus
  refreshProgress: Record<string, number>
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

export interface FileItem {
  name: string
  path: string
  type: 'file' | 'directory'
  size: number
  modTime: string
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

export interface SymlinkStore {
  verifySymlinks(): Promise<void>
  createSymlink(sourcePath: string): Promise<void>
  removeSymlink(targetPath: string): Promise<void>
  rebuildSymlinks(): Promise<void>
  clearSymlinks(): Promise<void>
  updateProgress(current: number, total: number, message?: string): void
}

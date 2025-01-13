export interface EmbyLibrary {
  id: string
  name: string
  path: string
  type: string
  lastScan?: string
  refreshing?: boolean
}

export interface EmbyStatus {
  connected: boolean
  version: string
  lastUpdate?: string
}

export interface RefreshProgress {
  libraryId: string
  percentage: number
  status: 'pending' | 'processing' | 'success' | 'error'
}

export interface EmbyStatus {
  serverStatus: 'connected' | 'disconnected'
  apiStatus: boolean
  version?: string
  lastCheck?: string
  lastUpdate?: string
}

export interface EmbyLibrary {
  id: string
  name: string
  path: string
  type: string
  itemCount?: number
  lastUpdate?: string
  refreshing?: boolean
}

export interface EmbyState {
  status: EmbyStatus
  libraries: EmbyLibrary[]
  refreshProgress: Record<string, number>
}

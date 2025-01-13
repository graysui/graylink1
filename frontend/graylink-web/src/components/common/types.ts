export interface ProgressBarProps {
  percentage: number
  status?: 'success' | 'warning' | 'exception'
  title?: string
  detail?: string
  current?: number
  total?: number
}

export interface StatusIndicatorProps {
  status: 'success' | 'warning' | 'error' | 'info'
  text?: string
  detail?: string
  effect?: 'light' | 'dark' | 'plain'
}

export interface PathSelectorProps {
  modelValue: string
  rootPath?: string
  placeholder?: string
  createDir?: boolean
} 
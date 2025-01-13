export function formatFileSize(bytes: number): number {
  if (bytes === 0) return 0
  const k = 1024
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return Number((bytes / Math.pow(k, i)).toFixed(2))
}

export function formatFileSizeWithUnit(bytes: number): string {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return `${(bytes / Math.pow(k, i)).toFixed(2)} ${sizes[i]}`
}

export function formatTime(time: string | number | Date): string {
  const date = new Date(time)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

export { formatTime as formatDateTime } 
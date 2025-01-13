import { useErrorStore } from '@/stores/modules/error'

export function handleError(error: unknown) {
  const errorStore = useErrorStore()
  errorStore.setError(error)
}

export function setupErrorHandling() {
  // 全局错误处理
  window.onerror = (message, source, line, column, error) => {
    console.error('Global error:', { message, source, line, column, error })
    handleError(error || message)
    return true
  }

  // Promise错误处理
  window.addEventListener('unhandledrejection', (event) => {
    console.error('Unhandled promise rejection:', event.reason)
    handleError(event.reason)
  })
} 
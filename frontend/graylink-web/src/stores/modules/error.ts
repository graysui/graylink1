import { defineStore } from 'pinia'
import { ref } from 'vue'

export interface ErrorInfo {
  message: string
  stack?: string
  code?: string | number
}

export const useErrorStore = defineStore('error', () => {
  const error = ref<ErrorInfo | null>(null)

  const setError = (err: unknown) => {
    if (err instanceof Error) {
      error.value = {
        message: err.message,
        stack: err.stack
      }
    } else if (typeof err === 'string') {
      error.value = {
        message: err
      }
    } else {
      error.value = {
        message: '未知错误'
      }
    }
  }

  const clearError = () => {
    error.value = null
  }

  return {
    error,
    setError,
    clearError
  }
}) 
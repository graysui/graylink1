import { AxiosRequestConfig } from 'axios'

declare module 'axios' {
  export interface AxiosRequestConfig {
    showLoading?: boolean
    retry?: number
    retryDelay?: number
    __retryCount?: number
  }
} 
import axios from 'axios'
import type { 
  AxiosRequestConfig as BaseAxiosRequestConfig,
  AxiosResponse as BaseAxiosResponse,
  AxiosInterceptorManager,
  InternalAxiosRequestConfig
} from 'axios'
import type { ApiResponse } from './api'

export interface AxiosRequestConfig extends BaseAxiosRequestConfig {
  headers?: Record<string, string>
  params?: Record<string, any>
  baseURL?: string
  timeout?: number
  showLoading?: boolean
  retry?: number
  retryDelay?: number
  __retryCount?: number
}

export interface AxiosResponse<T = any> extends BaseAxiosResponse<T> {}

declare module 'axios' {
  export interface AxiosInstance {
    request<T = any>(config: AxiosRequestConfig): Promise<AxiosResponse<ApiResponse<T>>>
    get<T = any>(url: string, config?: AxiosRequestConfig): Promise<AxiosResponse<ApiResponse<T>>>
    post<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<AxiosResponse<ApiResponse<T>>>
    put<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<AxiosResponse<ApiResponse<T>>>
    delete<T = any>(url: string, config?: AxiosRequestConfig): Promise<AxiosResponse<ApiResponse<T>>>
    interceptors: {
      request: AxiosInterceptorManager<InternalAxiosRequestConfig>
      response: AxiosInterceptorManager<AxiosResponse>
    }
  }

  export interface AxiosStatic extends AxiosInstance {
    create(config?: AxiosRequestConfig): AxiosInstance
    isAxiosError(payload: any): payload is AxiosError
    CancelToken: CancelTokenStatic
    isCancel(value: any): boolean
  }

  const axios: AxiosStatic
  export default axios
} 
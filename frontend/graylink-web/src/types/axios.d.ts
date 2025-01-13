import type { 
  AxiosRequestConfig as BaseAxiosRequestConfig,
  AxiosResponse as BaseAxiosResponse,
  AxiosInterceptorManager,
  InternalAxiosRequestConfig
} from 'axios'
import type { ApiResponse } from './api'

declare module 'axios' {
  export interface AxiosRequestConfig extends BaseAxiosRequestConfig {
    baseURL?: string
    timeout?: number
    headers?: Record<string, string>
    params?: Record<string, any>
  }

  export interface AxiosInstance {
    request<T = any>(config: AxiosRequestConfig): Promise<T>
    get<T = any>(url: string, config?: AxiosRequestConfig): Promise<T>
    post<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T>
    put<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T>
    delete<T = any>(url: string, config?: AxiosRequestConfig): Promise<T>
    interceptors: {
      request: AxiosInterceptorManager<InternalAxiosRequestConfig>
      response: AxiosInterceptorManager<AxiosResponse<any>>
    }
  }
} 
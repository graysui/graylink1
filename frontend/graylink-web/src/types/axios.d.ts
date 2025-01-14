import type { ApiResponse } from './response'

declare module 'axios' {
  export interface AxiosRequestConfig {
    baseURL?: string
    timeout?: number
    headers?: Record<string, string>
    params?: Record<string, any>
    data?: any
    method?: string
    url?: string
    responseType?: string
  }

  export interface AxiosInstance {
    request<T = any>(config: AxiosRequestConfig): Promise<ApiResponse<T>>
    get<T = any>(url: string, config?: AxiosRequestConfig): Promise<ApiResponse<T>>
    post<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<ApiResponse<T>>
    put<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<ApiResponse<T>>
    delete<T = any>(url: string, config?: AxiosRequestConfig): Promise<ApiResponse<T>>
  }
}

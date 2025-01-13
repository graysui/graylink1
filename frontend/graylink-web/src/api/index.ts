import axios from 'axios'
import type { AxiosInstance, AxiosRequestConfig } from 'axios'

// 使用正确的类型导入
interface AxiosResponse<T = any> {
  data: T
  status: number
  statusText: string
  headers: Record<string, string>
  config: AxiosRequestConfig
  request?: any
}

// 定义API响应类型
export interface ApiResponse<T = any> {
  code: number
  data: T
  message: string
}

export const api: AxiosInstance = axios.create({
  baseURL: '/api',
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 请求拦截器
api.interceptors.request.use(
  (config: AxiosRequestConfig) => {
    const token = localStorage.getItem('token')
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error: unknown) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  (response: AxiosResponse<ApiResponse>) => response.data,
  (error: unknown) => {
    return Promise.reject(error)
  }
)

// 创建专门的API实例
export const embyApi = api
export const fileApi = api
export const symlinkApi = api

// 添加API方法类型
declare module 'axios' {
  interface AxiosInstance {
    checkStatus(): Promise<ApiResponse>
    getLibraries(): Promise<ApiResponse>
    refreshByPaths(paths: string[]): Promise<ApiResponse>
    refreshRoot(): Promise<ApiResponse>
    getSnapshot(path?: string): Promise<ApiResponse>
    getStats(): Promise<ApiResponse>
    cleanup(): Promise<ApiResponse>
    verify(): Promise<ApiResponse>
    create(path: string): Promise<ApiResponse>
    remove(path: string): Promise<ApiResponse>
    rebuild(): Promise<ApiResponse>
    clear(): Promise<ApiResponse>
  }
}

import request from '@/utils/request'
import type { AxiosRequestConfig } from 'axios'
import type { ApiResponse } from '@/types/api'
import { embyApi } from './emby'

export * from './file'
export * from './monitor'
export * from './symlink'
export { embyApi }
export * from './setting'

// 基础请求方法
export async function get<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
  return await request.get<T>(url, config)
}

export async function post<T>(url: string, data?: unknown, config?: AxiosRequestConfig): Promise<T> {
  return await request.post<T>(url, data, config)
}

export async function put<T>(url: string, data?: unknown, config?: AxiosRequestConfig): Promise<T> {
  return await request.put<T>(url, data, config)
}

export async function del<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
  return await request.delete<T>(url, config)
} 
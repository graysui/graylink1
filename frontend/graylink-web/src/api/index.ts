import axios from 'axios'
import type { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios'
import type { ApiResponse } from '@/types/response'

// 创建API实例
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
  (response: AxiosResponse) => {
    const apiResponse = response.data as ApiResponse<unknown>
    if (apiResponse.code !== 0) {
      throw new Error(apiResponse.message)
    }
    return apiResponse.data
  },
  (error: unknown) => {
    return Promise.reject(error)
  }
)

// 创建专门的API实例
export const embyApi = api
export const fileApi = api
export const symlinkApi = api

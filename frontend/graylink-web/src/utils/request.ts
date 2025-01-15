import axios from 'axios'
import type { AxiosRequestConfig, AxiosResponse } from 'axios'
import type { ApiResponse } from '@/types/api'
import { getToken } from '@/utils/auth'

export const request = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  timeout: 10000
})

// 请求拦截器
request.interceptors.request.use(
  (config: AxiosRequestConfig) => {
    const token = getToken()
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error: Error) => Promise.reject(error)
)

// 响应拦截器
request.interceptors.response.use(
  (response: AxiosResponse) => {
    const apiResponse = response.data
    if (apiResponse.code !== 0) {
      throw new Error(apiResponse.message || '请求失败')
    }
    return apiResponse
  },
  (error: any) => {
    if (error.response?.data?.message) {
      throw new Error(error.response.data.message)
    }
    throw error
  }
)

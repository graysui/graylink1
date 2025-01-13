import axios from 'axios'
import type { AxiosInstance, InternalAxiosRequestConfig } from 'axios'
import type { ApiResponse } from '@/types/api'

interface CustomAxiosRequestConfig extends InternalAxiosRequestConfig {
  withCredentials?: boolean
}

const service: AxiosInstance = axios.create({
  baseURL: '/api',
  timeout: 15000,
  withCredentials: true
} as CustomAxiosRequestConfig)

service.interceptors.response.use(
  <T>(response: { data: ApiResponse<T> }) => {
    return response.data
  },
  (error: any) => {
    return Promise.reject(error)
  }
)

export default service 
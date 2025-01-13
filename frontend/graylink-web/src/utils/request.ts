import axios from 'axios'
import type { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios'
import { ElMessage } from 'element-plus'
import { handleError } from './error'

const service: AxiosInstance = axios.create({
  baseURL: '/api',
  timeout: 15000,
  withCredentials: true
})

// 请求拦截器
service.interceptors.request.use(
  (config) => {
    // 添加token等认证信息
    return config
  },
  (error) => {
    handleError(error)
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  (response: AxiosResponse) => {
    const { data } = response
    
    // 处理业务错误
    if (data.code && data.code !== 200) {
      const error = new Error(data.message || '请求失败')
      handleError(error)
      return Promise.reject(error)
    }
    
    return data
  },
  (error) => {
    // 处理网络错误
    let message = '网络错误'
    if (error.response) {
      switch (error.response.status) {
        case 401:
          message = '未授权，请重新登录'
          // 可以在这里处理登录过期
          break
        case 403:
          message = '拒绝访问'
          break
        case 404:
          message = '请求错误，未找到该资源'
          break
        case 500:
          message = '服务器错误'
          break
        default:
          message = error.response.data?.message || `连接错误${error.response.status}`
      }
    }
    
    ElMessage.error(message)
    handleError(error)
    return Promise.reject(error)
  }
)

export default service 
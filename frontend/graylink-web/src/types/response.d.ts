export interface ApiResponse<T = any> {
  code: number
  data: T
  message: string
  status?: string
}

export interface ErrorResponse {
  error: string
  message: string
  status: number
}

export interface PaginationData<T> {
  items: T[]
  total: number
  page: number
  pageSize: number
}

export interface PaginatedResponse<T> extends Omit<ApiResponse<any>, 'data'> {
  data: PaginationData<T>
}

// 扩展 axios 类型
declare module 'axios' {
  export interface AxiosResponse<T = any> {
    data: ApiResponse<T>
    status: number
    statusText: string
    headers: Record<string, string>
    config: AxiosRequestConfig
  }
}

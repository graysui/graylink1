import request from '@/utils/request'
import type { ApiResponse, UserInfo } from '@/types/api'
import type { LoginForm } from '@/stores/types'

interface LoginResponse {
  token: string
  username: string
  userInfo: {
    roles: string[]
    permissions: string[]
  }
}

export const userApi = {
  login(data: LoginForm) {
    return request.post<ApiResponse<LoginResponse>>('/auth/login', data)
  },

  register(data: LoginForm) {
    return request.post<ApiResponse<void>>('/auth/register', data)
  },

  logout() {
    return request.post<ApiResponse<void>>('/auth/logout')
  },

  getInfo() {
    return request.get<ApiResponse<UserInfo>>('/user/info')
  },

  changePassword(data: { new_password: string }) {
    return request.post<ApiResponse<void>>('/user/change-password', data)
  }
} 
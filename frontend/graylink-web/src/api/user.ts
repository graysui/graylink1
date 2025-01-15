import { request } from '@/utils/request'
import type { ApiResponse } from '@/types/api'

interface LoginForm {
  username: string
  password: string
}

interface UserProfile {
  username: string
  created_at: string
  updated_at: string
}

export const userApi = {
  login: (data: LoginForm) =>
    request.post<ApiResponse<void>>('/api/auth/login', data),

  register: (data: LoginForm) =>
    request.post<ApiResponse<void>>('/api/auth/register', data),

  logout: () =>
    request.post<ApiResponse<void>>('/api/auth/logout'),

  getProfile: () =>
    request.get<ApiResponse<UserProfile>>('/api/auth/profile'),

  updateProfile: (data: Partial<LoginForm>) =>
    request.post<ApiResponse<void>>('/api/auth/profile', data)
}

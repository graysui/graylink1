import request from '@/utils/request'
import type { UserInfo } from '@/types/api'

interface LoginResponse {
  token: string
  user: UserInfo
}

export const userApi = {
  login: (username: string, password: string) => 
    request.post<LoginResponse>('/auth/login', { username, password }),
    
  logout: () => request.post('/auth/logout'),
  
  getUserInfo: () => request.get<UserInfo>('/auth/user'),
  
  changePassword(data: {
    old_password: string
    new_password: string
  }) {
    return request.post('/user/change-password', data)
  }
} 
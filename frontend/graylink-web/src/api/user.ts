import { api } from '@/utils/request'
import type { LoginForm } from '@/types/auth'

export const userApi = {
  login: (data: LoginForm) => api.post('/auth/login', data),
  register: (data: LoginForm) => api.post('/auth/register', data),
  logout: () => api.post('/auth/logout'),
  getProfile: () => api.get('/auth/profile'),
  updateProfile: (data: Partial<LoginForm>) => api.post('/auth/profile', data)
}

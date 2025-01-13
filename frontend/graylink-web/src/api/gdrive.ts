import request from '@/utils/request'

export const gdriveApi = {
  // 获取授权 URL
  getAuthUrl() {
    return request.get<{ auth_url: string }>('/gdrive/auth-url')
  },

  // 开始设备授权流程
  startAuth() {
    return request.post<{
      user_code: string
      verification_url: string
      device_code: string
      expires_in: number
    }>('/gdrive/start-auth')
  },

  // 检查授权状态
  checkAuth(device_code: string) {
    return request.post<{ status: string }>('/gdrive/check-auth', { device_code })
  },

  // 测试连接
  test() {
    return request.post('/gdrive/test')
  }
} 
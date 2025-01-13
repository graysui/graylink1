import request from '@/utils/request'

export const gdriveApi = {
  // 开始设备授权
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
  }
} 
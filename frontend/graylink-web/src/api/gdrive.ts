import { api } from '@/utils/request'
import type { ApiResponse, ActivityResult, DriveActivity } from '@/types/api'

export const gdriveApi = {
  // 获取授权 URL
  getAuthUrl() {
    return api.get<ApiResponse<{ auth_url: string }>>('/gdrive/auth-url')
  },

  // 开始设备授权流程
  startAuth() {
    return api.post<ApiResponse<{
      user_code: string
      verification_url: string
      device_code: string
      expires_in: number
    }>>('/gdrive/start-auth')
  },

  // 检查授权状态
  checkAuth(device_code: string) {
    return api.post<ApiResponse<{ status: string }>>('/gdrive/check-auth', { device_code })
  },

  checkActivities() {
    return api.get<ApiResponse<ActivityResult>>('/gdrive/check-activities')
  },

  // 测试连接
  test() {
    return api.get<ApiResponse<void>>('/gdrive/test')
  }
}

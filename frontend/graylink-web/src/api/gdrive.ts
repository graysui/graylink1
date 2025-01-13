import request from '@/utils/request'
import type { ApiResponse, ActivityResult, DriveActivity } from '@/types/api'

export const gdriveApi = {
  // 获取授权 URL
  getAuthUrl() {
    return request.get<ApiResponse<{ auth_url: string }>>('/gdrive/auth-url')
  },

  // 开始设备授权流程
  startAuth() {
    return request.post<ApiResponse<{
      user_code: string
      verification_url: string
      device_code: string
      expires_in: number
    }>>('/gdrive/start-auth')
  },

  // 检查授权状态
  checkAuth(device_code: string) {
    return request.post<ApiResponse<{ status: string }>>('/gdrive/check-auth', { device_code })
  },

  checkActivities() {
    return request.get<ApiResponse<ActivityResult>>('/gdrive/check-activities')
  },

  // 测试连接
  test() {
    return request.get<ApiResponse<void>>('/gdrive/test')
  }
} 
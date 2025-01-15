import type { ApiResponse, ActivityResult } from '@/types/api'
import { request } from '@/utils/request'

export const gdriveApi = {
  // 获取授权URL
  getAuthUrl(): Promise<ApiResponse<string>> {
    return request.get('/api/gdrive/auth/url')
  },

  // 开始授权
  startAuth(code: string): Promise<ApiResponse<void>> {
    return request.post('/api/gdrive/auth/start', { code })
  },

  // 检查授权状态
  checkAuth(): Promise<ApiResponse<boolean>> {
    return request.get('/api/gdrive/auth/check')
  },

  // 检查活动
  checkActivities(pageToken?: string): Promise<ApiResponse<ActivityResult>> {
    return request.get('/api/gdrive/activities', {
      params: { page_token: pageToken }
    })
  },

  // 测试配置
  test(clientId: string, clientSecret: string): Promise<ApiResponse<void>> {
    return request.post('/api/gdrive/test', {
      client_id: clientId,
      client_secret: clientSecret
    })
  }
}

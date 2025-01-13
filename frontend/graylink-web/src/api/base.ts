import type { ApiResponse } from '@/types/response'

export function unwrapResponse<T>(response: ApiResponse<T>): T {
  if (response.code !== 0) {
    throw new Error(response.message)
  }
  return response.data
} 
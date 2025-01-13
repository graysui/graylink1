import { ElMessage } from 'element-plus'
import type { MessageParams } from 'element-plus'

export const showMessage = (
  message: string,
  type: 'success' | 'warning' | 'error' = 'success'
) => {
  ElMessage({
    message,
    type,
    duration: 2000
  })
}

export const showSuccess = (message: string) => showMessage(message, 'success')
export const showError = (message: string) => showMessage(message, 'error')
export const showWarning = (message: string) => showMessage(message, 'warning') 
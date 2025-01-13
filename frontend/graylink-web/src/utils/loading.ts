import { ElLoading } from 'element-plus'
import type { LoadingInstance } from 'element-plus/es/components/loading/src/loading'

class LoadingManager {
  private loadingInstance: LoadingInstance | null = null
  private loadingCount = 0
  private loadingTimer: number | null = null

  show(text = '加载中...') {
    this.loadingCount++

    // 防抖，避免频繁创建和销毁
    if (this.loadingTimer) {
      window.clearTimeout(this.loadingTimer)
    }

    if (!this.loadingInstance) {
      this.loadingTimer = window.setTimeout(() => {
        this.loadingInstance = ElLoading.service({
          lock: true,
          text,
          background: 'rgba(0, 0, 0, 0.7)'
        })
      }, 300) // 300ms 延迟显示
    }
  }

  hide() {
    this.loadingCount = Math.max(0, this.loadingCount - 1)

    if (this.loadingCount === 0) {
      if (this.loadingTimer) {
        window.clearTimeout(this.loadingTimer)
        this.loadingTimer = null
      }

      if (this.loadingInstance) {
        this.loadingInstance.close()
        this.loadingInstance = null
      }
    }
  }

  // 强制重置状态
  reset() {
    this.loadingCount = 0
    if (this.loadingTimer) {
      window.clearTimeout(this.loadingTimer)
      this.loadingTimer = null
    }
    if (this.loadingInstance) {
      this.loadingInstance.close()
      this.loadingInstance = null
    }
  }
}

const loadingManager = new LoadingManager()

export const showLoading = loadingManager.show.bind(loadingManager)
export const hideLoading = loadingManager.hide.bind(loadingManager)
export const resetLoading = loadingManager.reset.bind(loadingManager) 
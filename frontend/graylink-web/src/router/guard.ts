import type { Router, RouteLocationNormalized } from 'vue-router'
import NProgress from 'nprogress'
import { useUserStore } from '@/stores/modules/user'
import { useErrorStore } from '@/stores/modules/error'

export function setupRouterGuard(router: Router) {
  const errorStore = useErrorStore()

  router.beforeEach(async (to: RouteLocationNormalized, from: RouteLocationNormalized, next) => {
    NProgress.start()

    try {
      const userStore = useUserStore()
      
      if (to.meta.requiresAuth && !userStore.hasToken) {
        next({
          path: '/login',
          query: { redirect: to.fullPath }
        })
        return
      }

      if (to.meta.roles && !userStore.hasRoles(to.meta.roles)) {
        next({ path: '/403' })
        return
      }

      if (to.meta.title) {
        document.title = `${to.meta.title} - ${import.meta.env.VITE_APP_TITLE}`
      }

      next()
    } catch (error) {
      errorStore.setError(error as Error)
      NProgress.done()
      next(false)
    }
  })

  router.afterEach(() => {
    NProgress.done()
  })

  router.onError((error: Error) => {
    console.error('路由错误:', error)
    errorStore.setError(error)
    NProgress.done()
  })
} 
import type { Router, RouteLocationRaw } from 'vue-router'
import { useUserStore } from '@/stores/modules/user'

export function setupGuard(router: Router) {
  router.beforeEach(async (to, from, next) => {
    const userStore = useUserStore()

    if (to.meta.requiresAuth) {
      if (!userStore.hasToken) {
        next({
          path: '/login',
          query: { redirect: to.fullPath }
        } as RouteLocationRaw)
        return
      }

      if (to.meta.roles && !userStore.hasRoles(to.meta.roles)) {
        next({ path: '/403' } as RouteLocationRaw)
        return
      }
    }

    next()
  })
} 
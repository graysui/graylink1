import type { RouteLocationNormalized } from 'vue-router'
import { useUserStore } from '@/stores/modules/user'
import { useErrorStore } from '@/stores/modules/error'

// 路由元信息类型定义
declare module 'vue-router' {
  interface RouteMeta {
    title?: string
    requiresAuth?: boolean
    adminOnly?: boolean
  }
}

// 权限检查函数
export function checkPermission(route: RouteLocationNormalized) {
  const userStore = useUserStore()
  const { role } = userStore.userInfo || {}

  // 检查是否需要管理员权限
  if (route.meta.adminOnly) {
    return role === 'admin'
  }

  return true
}

// 登录重定向处理
export function handleLoginRedirect(to: RouteLocationNormalized) {
  const userStore = useUserStore()
  const errorStore = useErrorStore()

  if (!userStore.hasToken && to.meta.requiresAuth) {
    errorStore.setError(new Error('请先登录'))
    return {
      path: '/login',
      query: { redirect: to.fullPath }
    }
  }

  if (userStore.hasToken && !checkPermission(to)) {
    errorStore.setError(new Error('无访问权限'))
    return { path: '/403' }
  }

  return true
}

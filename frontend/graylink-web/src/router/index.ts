import { createRouter, createWebHistory, type Router } from 'vue-router'
import type { RouteRecordRaw, RouterOptions, RouteLocationRaw } from 'vue-router'
import { routes } from './routes'

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    }
    return { left: 0, top: 0 }
  }
} as RouterOptions)

// 确保 router 实例包含所有必要的方法
declare module 'vue-router' {
  interface Router {
    replace(to: RouteLocationRaw): Promise<void>
    push(to: RouteLocationRaw): Promise<void>
  }
}

export default router as Router 
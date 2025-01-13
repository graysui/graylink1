import { createRouter, createWebHistory } from 'vue-router'
import type { Router, RouteRecordRaw, RouteLocationRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  // ... 你的路由配置
]

const router = createRouter({
  history: createWebHistory(),
  routes,
}) as Router & {
  push: (to: RouteLocationRaw) => Promise<void>
  replace: (to: RouteLocationRaw) => Promise<void>
}

export default router

import { createRouter, createWebHistory } from 'vue-router'
import type { Router, RouteRecordRaw, RouteLocationRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/login/index.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/file',
    name: 'File',
    component: () => import('@/views/file/index.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/emby',
    name: 'Emby',
    component: () => import('@/views/emby/index.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
}) as Router & {
  push: (to: RouteLocationRaw) => Promise<void>
  replace: (to: RouteLocationRaw) => Promise<void>
}

export default router

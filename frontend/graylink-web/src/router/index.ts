import { createRouter, createWebHistory } from 'vue-router'
import type { Router, RouteRecordRaw, RouteLocationRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Root',
    component: () => import('@/views/file/index.vue'),
    meta: { requiresAuth: true }
  },
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
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/error/404.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
}) as Router & {
  push: (to: RouteLocationRaw) => Promise<void>
  replace: (to: RouteLocationRaw) => Promise<void>
}

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')

  if (to.meta.requiresAuth && !token) {
    next({
      path: '/login',
      query: { redirect: to.fullPath }
    })
  } else if (to.path === '/login' && token) {
    next({ path: '/file' })
  } else {
    next()
  }
})

export default router

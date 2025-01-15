import { createRouter, createWebHistory } from 'vue-router'
import type { Router } from 'vue-router'
import { routes } from './types'

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')

  if (to.meta.requiresAuth && !token) {
    next({
      path: '/login',
      query: { redirect: to.fullPath }
    })
  } else if (to.path === '/login' && token) {
    next({ path: '/monitor' })
  } else {
    next()
  }
})

export default router

import type { RouteRecordRaw } from 'vue-router'

interface CustomRouteRecordRaw extends Omit<RouteRecordRaw, 'redirect'> {
  redirect?: string
  meta?: {
    title?: string
    icon?: string
    requiresAuth?: boolean
    roles?: string[]
  }
}

export const routes: CustomRouteRecordRaw[] = [
  {
    path: '/',
    name: 'Root',
    component: () => import('@/views/layout/BasicLayout.vue'),
    redirect: '/monitor',
    meta: {
      requiresAuth: true
    },
    children: [
      {
        path: 'monitor',
        name: 'Monitor',
        component: () => import('@/views/monitor/index.vue'),
        meta: {
          title: '监控中心',
          icon: 'Monitor'
        }
      }
    ]
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/login/index.vue'),
    meta: {
      title: '登录'
    }
  }
] 
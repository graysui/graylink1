import type { RouteRecordRaw } from 'vue-router'

export const routes: RouteRecordRaw[] = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/login/index.vue'),
    meta: {
      title: '登录',
      requiresAuth: false
    }
  },
  {
    path: '/',
    component: () => import('@/components/layout/BasicLayout.vue'),
    meta: {
      requiresAuth: true
    },
    children: [
      {
        path: '',
        name: 'monitor',
        component: () => import('@/views/monitor/index.vue'),
        meta: {
          title: '监控中心',
          icon: 'Monitor'
        }
      },
      {
        path: 'emby',
        name: 'emby',
        component: () => import('@/views/emby/index.vue'),
        meta: {
          title: 'Emby管理',
          icon: 'VideoPlay'
        }
      },
      {
        path: 'symlink',
        name: 'symlink',
        component: () => import('@/views/symlink/index.vue'),
        meta: {
          title: '软链接管理',
          icon: 'Link'
        }
      },
      {
        path: 'setting',
        name: 'setting',
        component: () => import('@/views/setting/index.vue'),
        meta: {
          title: '系统设置',
          icon: 'Setting'
        }
      }
    ]
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/error/404.vue'),
    meta: {
      title: '页面未找到',
      requiresAuth: false
    }
  }
] 
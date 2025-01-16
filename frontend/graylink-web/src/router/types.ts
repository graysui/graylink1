import type { RouteRecordRaw } from 'vue-router'

export interface RouteMeta {
  title?: string
  icon?: string
  requiresAuth?: boolean
  adminOnly?: boolean
  hidden?: boolean
  keepAlive?: boolean
}

// 扩展 vue-router 模块声明
declare module 'vue-router' {
  interface Router {
    push(to: RouteLocationRaw): Promise<void>
    replace(to: RouteLocationRaw): Promise<void>
  }

  interface RouteRecordRaw {
    redirect?: string | RouteLocationRaw
  }

  interface RouteLocationNormalized {
    meta: RouteMeta
    matched: RouteRecordRaw[]
    params: Record<string, string>
    query: Record<string, string>
    hash: string
    fullPath: string
  }
}

export type { RouteRecordRaw }

// 导出路由配置
export const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Root',
    component: () => import('@/layout/BasicLayout.vue'),
    redirect: '/monitor',
    meta: { requiresAuth: true },
    children: [
      {
        path: 'monitor',
        name: 'Monitor',
        component: () => import('@/views/monitor/index.vue'),
        meta: {
          requiresAuth: true,
          title: '监控管理',
          icon: 'Monitor'
        }
      },
      {
        path: 'file',
        name: 'File',
        component: () => import('@/views/file/index.vue'),
        meta: {
          requiresAuth: true,
          title: '文件管理',
          icon: 'Folder'
        }
      },
      {
        path: 'symlink',
        name: 'Symlink',
        component: () => import('@/views/symlink/index.vue'),
        meta: {
          requiresAuth: true,
          title: '软链接管理',
          icon: 'Link'
        }
      },
      {
        path: 'emby',
        name: 'Emby',
        component: () => import('@/views/emby/index.vue'),
        meta: {
          requiresAuth: true,
          title: 'Emby 管理',
          icon: 'VideoPlay'
        }
      },
      {
        path: 'setting',
        name: 'Setting',
        component: () => import('@/views/setting/index.vue'),
        meta: {
          requiresAuth: true,
          adminOnly: true,
          title: '系统设置',
          icon: 'Setting'
        }
      }
    ]
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/login/index.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/error/404.vue')
  }
]

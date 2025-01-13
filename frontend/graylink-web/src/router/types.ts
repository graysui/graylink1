import type { RouteRecordRaw } from 'vue-router'

export interface RouteMeta {
  title?: string
  icon?: string
  redirect?: string
  requiresAuth?: boolean
  roles?: string[]
  hidden?: boolean
}

// 扩展 vue-router 模块声明
declare module 'vue-router' {
  interface Router {
    push(to: RouteLocationRaw): Promise<void>
    replace(to: RouteLocationRaw): Promise<void>
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

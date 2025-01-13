import type { Component } from 'vue'

declare module 'vue-router' {
  export interface RouterOptions {
    history: RouterHistory
    routes: RouteRecordRaw[]
    scrollBehavior?: (
      to: RouteLocationNormalized,
      from: RouteLocationNormalized,
      savedPosition: { left: number; top: number } | null
    ) => { left: number; top: number } | void
  }

  export interface RouterHistory {
    base: string
    location: string
    state: any
  }

  export interface RouteLocationRaw {
    path?: string
    name?: string
    params?: Record<string, any>
    query?: Record<string, any>
    hash?: string
  }

  export interface RouteRecord {
    path: string
    name?: string | null
    meta: RouteMeta
    components: Record<string, Component>
    children: RouteRecord[]
  }

  export interface Router {
    beforeEach: (guard: NavigationGuard) => void
    afterEach: (guard: NavigationGuardAfter) => void
    onError: (handler: (error: Error) => void) => void
  }

  export interface RouteLocationNormalized {
    path: string
    name?: string | null
    params: Record<string, string>
    query: Record<string, string>
    hash: string
    fullPath: string
    matched: RouteRecord[]
    meta: RouteMeta
  }

  export interface RouteMeta {
    title?: string
    requiresAuth?: boolean
    roles?: string[]
    keepAlive?: boolean
    icon?: string
  }

  export type NavigationGuardNext = (to?: RouteLocationRaw | false | void) => void
  export type NavigationGuard = (
    to: RouteLocationNormalized,
    from: RouteLocationNormalized,
    next: NavigationGuardNext
  ) => Promise<void> | void

  export type NavigationGuardAfter = (
    to: RouteLocationNormalized,
    from: RouteLocationNormalized
  ) => void

  export interface RouteRecordRaw {
    path: string
    name?: string
    component: () => Promise<any>
    components?: Record<string, () => Promise<any>>
    children?: RouteRecordRaw[]
    meta?: RouteMeta
    props?: boolean | Record<string, any> | ((to: RouteLocationNormalized) => Record<string, any>)
  }

  export function createRouter(options: RouterOptions): Router
  export function createWebHistory(base?: string): RouterHistory
  export function useRouter(): Router
  export function useRoute(): RouteLocationNormalized
} 
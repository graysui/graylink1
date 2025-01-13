import type { 
  RouteRecordRaw, 
  Router as VueRouter,
  RouteLocationRaw,
  NavigationFailure,
  RouteLocationNormalized,
  RouteRecordNormalized
} from 'vue-router'

declare module 'vue-router' {
  export interface Router extends VueRouter {
    push(to: RouteLocationRaw): Promise<NavigationFailure | void | undefined>
    replace(to: RouteLocationRaw): Promise<NavigationFailure | void | undefined>
  }

  export interface RouteMeta {
    title?: string
    icon?: string
    requiresAuth?: boolean
    roles?: string[]
    permissions?: string[]
  }
} 
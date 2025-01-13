/// <reference types="vite/client" />
/// <reference types="element-plus/global" />

declare module 'vue-router' {
  interface RouteMeta {
    title?: string
    requiresAuth?: boolean
  }
}

declare module 'axios' {
  export interface AxiosRequestConfig {
    showLoading?: boolean
  }
}

interface ImportMetaEnv {
  readonly VITE_APP_TITLE: string
  readonly VITE_APP_API_BASE_URL: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
} 
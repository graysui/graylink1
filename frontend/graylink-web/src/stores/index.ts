import { createPinia } from 'pinia'
import type { App } from 'vue'
import type { Store } from 'pinia'

const pinia = createPinia()

interface StoreContext {
  store: Store<string, any>
}

// 状态重置插件
const resetPlugin = ({ store }: StoreContext) => {
  const initialState = JSON.parse(JSON.stringify(store.$state))
  store.$reset = () => {
    store.$patch(initialState)
  }
}

pinia.use(resetPlugin)

// 持久化插件
const persistPlugin = ({ store }: StoreContext) => {
  // 从 localStorage 恢复状态
  const persistedState = localStorage.getItem(`${store.$id}-state`)
  if (persistedState) {
    store.$patch(JSON.parse(persistedState))
  }

  // 监听状态变化并保存
  store.$subscribe((mutation: any, state: any) => {
    localStorage.setItem(`${store.$id}-state`, JSON.stringify(state))
  })
}

pinia.use(persistPlugin)

export function setupStore(app: App) {
  app.use(pinia)
}

export * from './modules/user'
export * from './modules/error'
export * from './modules/monitor'
export * from './modules/file'
export * from './modules/symlink'
export * from './modules/emby'
export * from './modules/setting'

export default pinia 
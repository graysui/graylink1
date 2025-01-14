import type { Component } from 'vue'

declare module 'element-plus/dist/locale/zh-cn.mjs' {
  import type { Language } from 'element-plus/es/locale'
  const zhCn: Language
  export default zhCn
}

declare module 'element-plus' {
  export interface FormInstance {
    validate: () => Promise<boolean>
    resetFields: () => void
    clearValidate: (props?: string | string[]) => void
  }

  export interface ElMessage {
    success(message: string): void
    warning(message: string): void
    info(message: string): void
    error(message: string): void
  }
}

declare module '@element-plus/icons-vue' {
  import type { Component } from 'vue'

  export interface IconComponent extends Component {
    name: string
  }

  export const User: IconComponent
  export const Lock: IconComponent
  export const Fold: IconComponent
  export const Expand: IconComponent
  export const ArrowDown: IconComponent
  export const Close: IconComponent
  export const Search: IconComponent
  export const List: IconComponent
  export const Grid: IconComponent
  export const Refresh: IconComponent
  export const Upload: IconComponent
  export const Download: IconComponent
}

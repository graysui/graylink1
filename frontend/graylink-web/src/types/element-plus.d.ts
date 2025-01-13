import type { Component } from 'vue'

declare module 'element-plus/dist/locale/zh-cn.mjs' {
  const zhCn: {
    name: 'zh-cn'
    el: Record<string, any>
  }
  export default zhCn
}

declare module 'element-plus' {
  export interface FormItemRule {
    required?: boolean
    message?: string
    trigger?: 'blur' | 'change' | ['blur', 'change']
    min?: number
    max?: number
    type?: string
    validator?: (rule: any, value: any, callback: any) => void
  }

  export interface FormInstance {
    validate: () => Promise<boolean>
    resetFields: () => void
    clearValidate: (props?: string | string[]) => void
  }

  export interface ElMessageOptions {
    message: string
    type?: 'success' | 'warning' | 'info' | 'error'
    duration?: number
    showClose?: boolean
  }

  export interface ElMessage {
    (options: ElMessageOptions | string): void
    success(message: string): void
    warning(message: string): void
    info(message: string): void
    error(message: string): void
  }

  export interface ElButtonProps {
    type?: 'primary' | 'success' | 'warning' | 'danger' | 'info' | 'text'
    size?: 'large' | 'default' | 'small'
    loading?: boolean
    disabled?: boolean
    icon?: string | Component
  }

  export interface ElSelectProps {
    modelValue: any
    multiple?: boolean
    disabled?: boolean
    clearable?: boolean
    placeholder?: string
    filterable?: boolean
  }

  export interface ElSwitchProps {
    modelValue: boolean
    disabled?: boolean
    activeText?: string
    inactiveText?: string
    activeValue?: string | number | boolean
    inactiveValue?: string | number | boolean
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

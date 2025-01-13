import type { FormItemRule } from 'element-plus'

declare module 'element-plus' {
  interface FormRules {
    [key: string]: FormItemRule | FormItemRule[]
  }
} 
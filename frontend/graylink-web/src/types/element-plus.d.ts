import type { Component } from 'vue'
import type { FormItemRule, FormInstance } from 'element-plus'

declare module 'element-plus/dist/locale/zh-cn.mjs' {
  const zhCn: {
    name: 'zh-cn'
    el: Record<string, any>
  }
  export default zhCn
}

declare module '@element-plus/icons-vue' {
  import type { Component } from 'vue'
  
  export interface IconComponent extends Component {
    name: string
  }

  export const InfoFilled: IconComponent
  export const ArrowDown: IconComponent
  export const Expand: IconComponent
  export const Fold: IconComponent
  // 添加其他需要的图标...
}

declare module 'element-plus' {
  export interface TagProps {
    type?: 'success' | 'warning' | 'info' | 'primary' | 'danger'
  }

  export interface StatisticProps {
    value: number | string
    title?: string
    precision?: number
  }

  export interface ProgressProps {
    percentage: number
    status?: 'success' | 'warning' | 'exception'
    indeterminate?: boolean
    duration?: number
    color?: string | Array<{ color: string; percentage: number }>
    width?: number
    strokeWidth?: number
    textInside?: boolean
    showText?: boolean
    format?: (percentage: number) => string
  }

  export interface FormRules {
    [key: string]: FormItemRule | FormItemRule[]
  }
} 
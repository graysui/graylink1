import type { Component } from 'vue'

declare module '@element-plus/icons-vue' {
  namespace ElementPlusIconsVue {
    interface IconComponent extends Component {
      name: string
    }

    export const Refresh: IconComponent
    export const Upload: IconComponent
    export const Download: IconComponent
    export const More: IconComponent
    export const FolderAdd: IconComponent
    export const Copy: IconComponent
    export const Delete: IconComponent
    export const FolderFilled: IconComponent
    export const Picture: IconComponent
    export const VideoCamera: IconComponent
    export const Headset: IconComponent
    export const Document: IconComponent
    export const Link: IconComponent
    export const Select: IconComponent
    export const Close: IconComponent
  }
} 
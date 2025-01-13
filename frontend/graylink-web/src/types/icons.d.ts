declare module '@element-plus/icons-vue' {
  import type { Component } from 'vue'
  
  export interface IconComponent extends Component {
    name: string
  }

  // 登录相关
  export const User: IconComponent
  export const Lock: IconComponent
  
  // 导航相关
  export const Fold: IconComponent
  export const Expand: IconComponent
  export const ArrowDown: IconComponent
  export const Close: IconComponent
  
  // 文件操作相关
  export const Download: IconComponent
  export const Upload: IconComponent
  export const Document: IconComponent
  export const FolderAdd: IconComponent
  export const Picture: IconComponent
  export const VideoCamera: IconComponent
  export const Headset: IconComponent
  export const More: IconComponent
  export const Folder: IconComponent
  
  // 状态相关
  export const InfoFilled: IconComponent
  export const Warning: IconComponent
  export const Check: IconComponent
  export const Delete: IconComponent
  
  // 其他操作
  export const Link: IconComponent
  export const Edit: IconComponent
  export const Plus: IconComponent
  export const Search: IconComponent
  export const Refresh: IconComponent
} 
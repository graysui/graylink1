# GrayLink Web Frontend

## 项目说明
GrayLink Web 是一个基于 Vue 3 + TypeScript + Element Plus 的前端项目。

## 类型系统重构
### 当前问题
1. **类型定义混乱**
   - 存在重复的定义文件
   - 同一模块有多个类型文件
   - 命名不统一

2. **类型检查问题**
   - verbatimModuleSyntax 开启但代码未完全适配
   - 前后端接口类型不匹配
   - 可选属性的空值检查不完整

3. **依赖管理问题**
   - 第三方库的类型定义不完整
   - 依赖版本管理不够严格

### 架构改进方案
1. **类型定义目录结构**
```
src/types/
  ├── api/          # API 相关类型
  │   ├── request.d.ts
  │   ├── response.d.ts
  │   └── modules/  # 按模块划分的 API 类型
  │       ├── file.d.ts
  │       ├── auth.d.ts
  │       └── ...
  ├── store/        # Store 相关类型
  │   ├── index.d.ts
  │   └── modules/
  │       ├── file.d.ts
  │       └── ...
  ├── components/   # 组件相关类型
  ├── utils/        # 工具相关类型
  └── vendor/       # 第三方库类型声明
      └── element-plus/
```

2. **类型规范**
   - 所有类型使用 type 关键字导入
   - 接口定义统一使用 .d.ts 后缀
   - 实现文件使用 .ts 后缀
   - API 响应类型与后端保持一致
   - 完整的空值检查

3. **依赖管理**
   - 使用 .npmrc 确保依赖版本一致
   - 锁定第三方库版本
   - 完整的类型声明文件

## 开发规范
1. **类型导入**
```typescript
// 正确示例
import type { LoginForm } from '@/types/api/modules/auth'
import type { FileOperations } from '@/types/store/modules/file'

// 错误示例
import { LoginForm } from '@/types/auth'
```

2. **空值检查**
```typescript
// 正确示例
function setSorting(by: keyof FileItem, desc: boolean) {
  files.value.sort((a, b) => {
    const aValue = a[by]
    const bValue = b[by]
    if (aValue === undefined || bValue === undefined) return 0
    return desc ? (aValue < bValue ? 1 : -1) : (aValue < bValue ? -1 : 1)
  })
}

// 错误示例
function setSorting(by: string, desc: boolean) {
  files.value.sort((a, b) => {
    const aValue = a[by as keyof FileItem]
    const bValue = b[by as keyof FileItem]
    return desc ? (aValue < bValue ? 1 : -1) : (aValue < bValue ? -1 : 1)
  })
}
```

3. **API 类型定义**
```typescript
// 正确示例
export interface ApiResponse<T> {
  code: number
  data: T
  message: string
}

// 错误示例
export interface ApiResponse {
  code: number
  data: any
  message: string
}
```

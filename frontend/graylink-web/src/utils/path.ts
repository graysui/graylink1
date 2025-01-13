/**
 * 路径工具函数
 */

// 验证路径格式
export function isValidPath(path: string): boolean {
  if (!path) return false
  
  // 必须以/开头
  if (!path.startsWith('/')) return false
  
  // 不允许包含 .. 或 连续的 /
  if (path.includes('..') || path.includes('//')) return false
  
  // 不允许特殊字符
  const invalidChars = /[<>:"|?*\x00-\x1F]/g
  return !invalidChars.test(path)
}

// 规范化路径
export function normalizePath(path: string): string {
  if (!path) return '/'
  
  // 确保以/开头
  path = path.startsWith('/') ? path : `/${path}`
  
  // 移除结尾的/（除了根路径）
  path = path === '/' ? path : path.replace(/\/+$/, '')
  
  // 规范化分隔符
  path = path.replace(/\/+/g, '/')
  
  return path
}

// 获取父路径
export function getParentPath(path: string): string {
  if (!path || path === '/') return '/'
  const normalized = normalizePath(path)
  return normalized.substring(0, normalized.lastIndexOf('/')) || '/'
}

// 获取路径名称
export function getPathName(path: string): string {
  if (!path || path === '/') return '/'
  const normalized = normalizePath(path)
  return normalized.substring(normalized.lastIndexOf('/') + 1)
}

// 拼接路径
export function joinPath(...paths: string[]): string {
  return normalizePath(paths.join('/'))
}

// 检查是否是子路径
export function isSubPath(parent: string, child: string): boolean {
  const normalizedParent = normalizePath(parent)
  const normalizedChild = normalizePath(child)
  
  if (normalizedParent === '/') return true
  if (normalizedChild === '/') return false
  
  return normalizedChild.startsWith(`${normalizedParent}/`)
}

// 获取相对路径
export function getRelativePath(from: string, to: string): string {
  const normalizedFrom = normalizePath(from)
  const normalizedTo = normalizePath(to)
  
  if (normalizedFrom === normalizedTo) return '.'
  if (normalizedFrom === '/') return normalizedTo.substring(1)
  if (isSubPath(normalizedFrom, normalizedTo)) {
    return normalizedTo.substring(normalizedFrom.length + 1)
  }
  
  const fromParts = normalizedFrom.split('/').filter(Boolean)
  const toParts = normalizedTo.split('/').filter(Boolean)
  
  let commonParts = 0
  while (commonParts < fromParts.length && commonParts < toParts.length) {
    if (fromParts[commonParts] !== toParts[commonParts]) break
    commonParts++
  }
  
  const upCount = fromParts.length - commonParts
  const relativeParts = Array(upCount).fill('..')
  relativeParts.push(...toParts.slice(commonParts))
  
  return relativeParts.join('/')
} 
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

interface LoginForm {
  username: string
  password: string
}

export const useUserStore = defineStore('user', () => {
  const token = ref<string | null>(null)
  const username = ref<string>('')
  
  // 默认管理员账户
  const defaultUser = {
    username: 'admin',
    password: 'admin'
  }

  // 登录功能
  const login = async (loginForm: LoginForm) => {
    if (loginForm.username === defaultUser.username && 
        loginForm.password === defaultUser.password) {
      token.value = 'admin-token'
      username.value = defaultUser.username
      return true
    }
    
    throw new Error('用户名或密码错误')
  }

  const logout = () => {
    token.value = null
    username.value = ''
  }

  const hasToken = computed(() => !!token.value)

  return {
    token,
    username,
    login,
    logout,
    hasToken
  }
}) 
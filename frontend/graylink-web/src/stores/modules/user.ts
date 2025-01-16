import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { UserState, LoginForm, UserInfo } from '../types'
import { userApi } from '@/api/user'

export const useUserStore = defineStore('user', () => {
  const token = ref<string | null>(null)
  const username = ref('')
  const userInfo = ref<UserInfo | null>(null)

  const hasToken = computed(() => !!token.value)
  const hasRoles = (roles: string[]) => {
    return userInfo.value?.role === 'admin'
  }

  const getUserInfo = async () => {
    try {
      const response = await userApi.getUserInfo()
      userInfo.value = response.data.data
      return response.data.data
    } catch (error) {
      console.error('Failed to get user info:', error)
      return null
    }
  }

  const login = async (form: LoginForm) => {
    const response = await userApi.login(form)
    const { token: tokenValue, username: usernameValue } = response.data.data
    token.value = tokenValue
    username.value = usernameValue
    if (tokenValue) {
      localStorage.setItem('token', tokenValue)
      await getUserInfo()
    }
  }

  const register = async (form: LoginForm) => {
    await userApi.register(form)
  }

  const logout = () => {
    token.value = null
    username.value = ''
    userInfo.value = null
    localStorage.removeItem('token')
  }

  return {
    token,
    username,
    userInfo,
    hasToken,
    hasRoles,
    getUserInfo,
    login,
    register,
    logout
  }
})

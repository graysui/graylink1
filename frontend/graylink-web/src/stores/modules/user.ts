import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { UserState, LoginForm } from '../types'
import { userApi } from '@/api/user'

export const useUserStore = defineStore('user', () => {
  const token = ref<string | null>(null)
  const username = ref('')
  const userInfo = ref<UserState['userInfo']['value']>(null)

  const hasToken = computed(() => !!token.value)
  const hasRoles = (roles: string[]) => {
    return userInfo.value?.roles.some(role => roles.includes(role)) ?? false
  }

  const login = async (form: LoginForm) => {
    const response = await userApi.login(form)
    const tokenValue = response.data.token
    token.value = tokenValue
    username.value = response.data.username
    userInfo.value = response.data.userInfo
    if (tokenValue) {
      localStorage.setItem('token', tokenValue)
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
    login,
    register,
    logout
  }
})

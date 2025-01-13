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
    const { data } = await userApi.login(form)
    token.value = data.token
    username.value = data.username
    userInfo.value = data.userInfo
  }

  const register = async (form: LoginForm) => {
    await userApi.register(form)
  }

  const logout = () => {
    token.value = null
    username.value = ''
    userInfo.value = null
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
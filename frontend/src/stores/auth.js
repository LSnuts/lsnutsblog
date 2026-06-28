import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authAPI } from '@/api'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || null)
  const refreshToken = ref(localStorage.getItem('refreshToken') || null)
  const user = ref(JSON.parse(localStorage.getItem('user') || 'null'))

  const isAuthenticated = computed(() => !!token.value)

  // 登录
  const login = async (credentials) => {
    const response = await authAPI.login(credentials)
    setAuth(response)
    return response
  }

  // 注册
  const register = async (userData) => {
    const response = await authAPI.register(userData)
    setAuth(response)
    return response
  }

  // 登出
  const logout = () => {
    token.value = null
    refreshToken.value = null
    user.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('refreshToken')
    localStorage.removeItem('user')
  }

  // 获取当前用户信息
  const fetchCurrentUser = async () => {
    if (!token.value) return null

    try {
      const response = await authAPI.getCurrentUser()
      user.value = response.user
      localStorage.setItem('user', JSON.stringify(response.user))
      return response.user
    } catch (error) {
      logout()
      throw error
    }
  }

  // 设置认证信息
  const setAuth = (data) => {
    token.value = data.access_token
    refreshToken.value = data.refresh_token
    user.value = data.user
    localStorage.setItem('token', data.access_token)
    localStorage.setItem('refreshToken', data.refresh_token)
    localStorage.setItem('user', JSON.stringify(data.user))
  }

  // 修改密码
  const changePassword = async (data) => {
    return await authAPI.changePassword(data)
  }

  return {
    token,
    refreshToken,
    user,
    isAuthenticated,
    login,
    register,
    logout,
    fetchCurrentUser,
    changePassword
  }
})
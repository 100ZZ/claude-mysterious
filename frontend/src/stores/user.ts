import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { User } from '@/types'
import { getCurrentUser } from '@/api/auth'

export const useUserStore = defineStore('user', () => {
  const user = ref<User | null>(null)
  const token = ref<string>(localStorage.getItem('token') || '')

  const setToken = (newToken: string) => {
    token.value = newToken
    localStorage.setItem('token', newToken)
  }

  const setUser = (newUser: User) => {
    user.value = newUser
  }

  const clearAuth = () => {
    token.value = ''
    user.value = null
    localStorage.removeItem('token')
  }

  const fetchUser = async () => {
    try {
      const userData = await getCurrentUser()
      setUser(userData)
      return userData
    } catch (error) {
      clearAuth()
      throw error
    }
  }

  const isAdmin = () => {
    return user.value?.username === 'admin'
  }

  return {
    user,
    token,
    setToken,
    setUser,
    clearAuth,
    fetchUser,
    isAdmin
  }
})


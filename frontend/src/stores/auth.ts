import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/services/api'

export interface User {
  id: number
  username: string
  email: string
  roles: string[]
}

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(localStorage.getItem('auth_token'))
  const isLoading = ref(false)

  const isAuthenticated = computed(() => !!token.value && !!user.value)
  const isAdmin = computed(() => user.value?.roles.includes('admin') ?? false)
  const isUser = computed(() => user.value?.roles.includes('user') ?? false)

  const login = async (username: string, password: string) => {
    isLoading.value = true
    try {
      const response = await api.post('/api/login', { username, password })
      token.value = response.data.auth_token
      localStorage.setItem('auth_token', token.value!)
      
      // Fetch user details
      await fetchUserDetails()
      
      return response.data
    } catch (error) {
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const register = async (username: string, email: string, password: string) => {
    isLoading.value = true
    try {
      const response = await api.post('/api/register', { username, email, password })
      return response.data
    } catch (error) {
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const fetchUserDetails = async () => {
    if (!token.value) return
    
    try {
      const response = await api.get('/api/home', {
        headers: { 'Authentication-Token': token.value }
      })
      user.value = {
        id: response.data.user_id || 0,
        username: response.data.username,
        email: response.data.email,
        roles: response.data.roles
      }
    } catch (error) {
      console.error('Failed to fetch user details:', error)
      logout()
    }
  }

  const logout = () => {
    user.value = null
    token.value = null
    localStorage.removeItem('auth_token')
  }

  const initializeAuth = async () => {
    if (token.value) {
      await fetchUserDetails()
    }
  }

  return {
    user,
    token,
    isLoading,
    isAuthenticated,
    isAdmin,
    isUser,
    login,
    register,
    logout,
    initializeAuth,
    fetchUserDetails
  }
})
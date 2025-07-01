import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/services/api'
import { useToast } from 'vue-toastification'

const toast = useToast()

export interface User {
  id: number
  username: string
  email: string
  role: string
  created_at: string
}

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(null)
  const loading = ref(false)

  const isAuthenticated = computed(() => !!token.value)
  const isAdmin = computed(() => user.value?.role === 'admin')

  const login = async (username: string, password: string) => {
    loading.value = true
    try {
      console.log('Attempting login with:', { username, password: '***' })
      
      const response = await api.post('/api/login', { username, password })
      console.log('Login response:', response.data)
      
      const { user: userData, auth_token } = response.data
      
      user.value = userData
      token.value = auth_token
      
      localStorage.setItem('token', auth_token)
      localStorage.setItem('user', JSON.stringify(userData))
      
      toast.success('Login successful!')
      return true
    } catch (error: any) {
      console.error('Login error:', error.response?.data || error.message)
      const errorMessage = error.response?.data?.message || error.response?.data?.error || 'Login failed'
      toast.error(errorMessage)
      return false
    } finally {
      loading.value = false
    }
  }

  const register = async (username: string, email: string, password: string) => {
    loading.value = true
    try {
      await api.post('/api/register', { username, email, password })
      toast.success('Registration successful! Please login.')
      return true
    } catch (error: any) {
      const errorMessage = error.response?.data?.error || error.response?.data?.message || 'Registration failed'
      toast.error(errorMessage)
      return false
    } finally {
      loading.value = false
    }
  }

  const logout = () => {
    user.value = null
    token.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    toast.success('Logged out successfully')
  }

  const checkAuth = () => {
    const storedToken = localStorage.getItem('token')
    const storedUser = localStorage.getItem('user')
    
    if (storedToken && storedUser) {
      token.value = storedToken
      user.value = JSON.parse(storedUser)
    }
  }

  return {
    user,
    token,
    loading,
    isAuthenticated,
    isAdmin,
    login,
    register,
    logout,
    checkAuth
  }
})
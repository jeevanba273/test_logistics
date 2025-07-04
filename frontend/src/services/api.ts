import axios from 'axios'
import { useToast } from 'vue-toastification'

const toast = useToast()

// Get API base URL from environment variables
const getApiBaseUrl = () => {
  if (import.meta.env.PROD) {
    return import.meta.env.VITE_API_BASE_URL || 'https://testlogistics-production.up.railway.app'
  }
  return '/api' // Use proxy in development
}

const api = axios.create({
  baseURL: getApiBaseUrl(),
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  }
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      // Use the correct header format for Flask-Security
      config.headers['Authentication-Token'] = token
    }
    console.log('API Request:', {
      url: config.url,
      method: config.method,
      headers: config.headers,
      data: config.data
    })
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  (response) => {
    console.log('API Response:', {
      url: response.config.url,
      status: response.status,
      data: response.data
    })
    return response
  },
  (error) => {
    console.error('API Error:', {
      url: error.config?.url,
      status: error.response?.status,
      data: error.response?.data,
      message: error.message
    })
    
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    } else if (error.response?.status >= 500) {
      toast.error('Server error occurred. Please try again later.')
    } else if (error.response?.data?.message) {
      toast.error(error.response.data.message)
    } else if (error.response?.data?.error) {
      toast.error(error.response.data.error)
    }
    return Promise.reject(error)
  }
)

export default api
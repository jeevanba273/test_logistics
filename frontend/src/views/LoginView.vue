<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-50 to-secondary-100">
    <div class="max-w-md w-full space-y-8 p-8">
      <div class="text-center animate-fade-in">
        <div class="flex justify-center mb-6">
          <div class="w-16 h-16 bg-primary-600 rounded-2xl flex items-center justify-center">
            <TruckIcon class="w-10 h-10 text-white" />
          </div>
        </div>
        <h2 class="text-3xl font-bold text-gray-900">Welcome back</h2>
        <p class="mt-2 text-sm text-gray-600">Sign in to your LogiTrack account</p>
      </div>

      <form @submit.prevent="handleLogin" class="mt-8 space-y-6 animate-slide-up">
        <div class="space-y-4">
          <div>
            <label for="username" class="block text-sm font-medium text-gray-700">Username</label>
            <input
              id="username"
              v-model="form.username"
              type="text"
              required
              class="input-field mt-1"
              placeholder="Enter your username"
            />
          </div>
          <div>
            <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
            <input
              id="password"
              v-model="form.password"
              type="password"
              required
              class="input-field mt-1"
              placeholder="Enter your password"
            />
          </div>
        </div>

        <div>
          <button
            type="submit"
            :disabled="authStore.isLoading"
            class="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="authStore.isLoading" class="flex items-center justify-center">
              <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Signing in...
            </span>
            <span v-else>Sign in</span>
          </button>
        </div>

        <div class="text-center">
          <p class="text-sm text-gray-600">
            Don't have an account?
            <router-link to="/register" class="font-medium text-primary-600 hover:text-primary-500">
              Sign up
            </router-link>
          </p>
        </div>
      </form>

      <!-- Demo Credentials -->
      <div class="mt-8 p-4 bg-gray-100 rounded-lg animate-fade-in">
        <h3 class="text-sm font-medium text-gray-700 mb-2">Demo Credentials:</h3>
        <div class="text-xs text-gray-600 space-y-1">
          <p><strong>Admin:</strong> admin01 / 1234</p>
          <p><strong>User:</strong> user01 / 1234</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useToast } from 'vue-toastification'
import { TruckIcon } from '@heroicons/vue/24/outline'

const router = useRouter()
const authStore = useAuthStore()
const toast = useToast()

const form = reactive({
  username: '',
  password: ''
})

const handleLogin = async () => {
  try {
    await authStore.login(form.username, form.password)
    toast.success('Login successful!')
    router.push('/dashboard')
  } catch (error: any) {
    toast.error(error.response?.data?.message || 'Login failed')
  }
}
</script>
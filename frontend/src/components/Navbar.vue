<template>
  <nav class="fixed top-0 left-0 h-full w-64 bg-white shadow-lg border-r border-gray-200 z-50">
    <div class="flex flex-col h-full">
      <!-- Logo -->
      <div class="flex items-center justify-center h-16 border-b border-gray-200">
        <div class="flex items-center space-x-2">
          <div class="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center">
            <TruckIcon class="w-5 h-5 text-white" />
          </div>
          <span class="text-xl font-bold text-gray-900">LogiTrack</span>
        </div>
      </div>

      <!-- Navigation Links -->
      <div class="flex-1 px-4 py-6 space-y-2">
        <router-link
          v-for="item in navigationItems"
          :key="item.name"
          :to="item.href"
          class="flex items-center px-3 py-2 text-sm font-medium rounded-lg transition-colors duration-200"
          :class="[
            $route.path === item.href
              ? 'bg-primary-50 text-primary-700 border-r-2 border-primary-600'
              : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
          ]"
        >
          <component :is="item.icon" class="w-5 h-5 mr-3" />
          {{ item.name }}
        </router-link>
      </div>

      <!-- User Profile -->
      <div class="border-t border-gray-200 p-4">
        <div class="flex items-center space-x-3 mb-3">
          <div class="w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center">
            <UserIcon class="w-5 h-5 text-primary-600" />
          </div>
          <div class="flex-1 min-w-0">
            <p class="text-sm font-medium text-gray-900 truncate">
              {{ authStore.user?.username }}
            </p>
            <p class="text-xs text-gray-500 truncate">
              {{ authStore.user?.email }}
            </p>
          </div>
        </div>
        <button
          @click="logout"
          class="w-full flex items-center px-3 py-2 text-sm font-medium text-red-600 hover:bg-red-50 rounded-lg transition-colors duration-200"
        >
          <ArrowRightOnRectangleIcon class="w-5 h-5 mr-3" />
          Logout
        </button>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import {
  HomeIcon,
  TruckIcon,
  DocumentTextIcon,
  PlusIcon,
  UserIcon,
  Cog6ToothIcon,
  ArrowRightOnRectangleIcon,
  ChartBarIcon
} from '@heroicons/vue/24/outline'

const router = useRouter()
const authStore = useAuthStore()

const navigationItems = computed(() => {
  const items = [
    { name: 'Dashboard', href: '/dashboard', icon: HomeIcon },
    { name: 'Transactions', href: '/transactions', icon: DocumentTextIcon },
    { name: 'Create Transaction', href: '/transactions/create', icon: PlusIcon },
    { name: 'Profile', href: '/profile', icon: UserIcon },
  ]

  if (authStore.isAdmin) {
    items.splice(1, 0, { name: 'Admin Panel', href: '/admin', icon: ChartBarIcon })
  }

  return items
})

const logout = () => {
  authStore.logout()
  router.push('/login')
}
</script>
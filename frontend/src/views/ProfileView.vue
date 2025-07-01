<template>
  <div class="p-6 max-w-2xl mx-auto">
    <div class="animate-fade-in">
      <h1 class="text-3xl font-bold text-gray-900 mb-2">Profile</h1>
      <p class="text-gray-600 mb-8">Manage your account information</p>
    </div>

    <div class="space-y-6">
      <!-- Profile Information -->
      <div class="card animate-slide-up">
        <div class="flex items-center space-x-4 mb-6">
          <div class="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center">
            <UserIcon class="w-8 h-8 text-primary-600" />
          </div>
          <div>
            <h2 class="text-xl font-semibold text-gray-900">{{ authStore.user?.username }}</h2>
            <p class="text-gray-600">{{ authStore.user?.email }}</p>
            <div class="flex space-x-2 mt-2">
              <span
                v-for="role in authStore.user?.roles"
                :key="role"
                class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-primary-100 text-primary-800"
              >
                {{ role }}
              </span>
            </div>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Username</label>
            <input
              :value="authStore.user?.username"
              type="text"
              disabled
              class="input-field bg-gray-50"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
            <input
              :value="authStore.user?.email"
              type="email"
              disabled
              class="input-field bg-gray-50"
            />
          </div>
        </div>
      </div>

      <!-- Account Statistics -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <StatsCard
          title="My Transactions"
          :value="userStats.totalTransactions"
          :icon="DocumentTextIcon"
          color="blue"
        />
        <StatsCard
          title="Total Spent"
          :value="`$${userStats.totalSpent.toLocaleString()}`"
          :icon="CurrencyDollarIcon"
          color="green"
        />
        <StatsCard
          title="Active Shipments"
          :value="userStats.activeShipments"
          :icon="TruckIcon"
          color="purple"
        />
      </div>

      <!-- Recent Activity -->
      <div class="card animate-slide-up">
        <h2 class="text-lg font-semibold text-gray-900 mb-4">Recent Activity</h2>
        <div v-if="recentTransactions.length === 0" class="text-center py-8">
          <DocumentTextIcon class="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <p class="text-gray-500">No recent activity</p>
        </div>
        <div v-else class="space-y-4">
          <div
            v-for="transaction in recentTransactions"
            :key="transaction.id"
            class="flex items-center justify-between p-4 bg-gray-50 rounded-lg"
          >
            <div>
              <p class="font-medium text-gray-900">{{ transaction.name }}</p>
              <p class="text-sm text-gray-600">
                {{ transaction.source_city }} → {{ transaction.destination_city }}
              </p>
            </div>
            <div class="text-right">
              <p class="font-medium text-gray-900">${{ transaction.amount.toLocaleString() }}</p>
              <span :class="getStatusClass(transaction.internal_status)" class="status-badge">
                {{ transaction.internal_status }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Actions -->
      <div class="card">
        <h2 class="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <router-link to="/transactions/create" class="btn-primary text-center">
            Create New Transaction
          </router-link>
          <router-link to="/transactions" class="btn-secondary text-center">
            View All Transactions
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useTransactionsStore } from '@/stores/transactions'
import StatsCard from '@/components/StatsCard.vue'
import {
  UserIcon,
  DocumentTextIcon,
  CurrencyDollarIcon,
  TruckIcon
} from '@heroicons/vue/24/outline'

const authStore = useAuthStore()
const transactionsStore = useTransactionsStore()

const userTransactions = computed(() => 
  transactionsStore.transactions.filter(t => t.user_id === authStore.user?.id)
)

const recentTransactions = computed(() => 
  userTransactions.value.slice(0, 5)
)

const userStats = computed(() => {
  const transactions = userTransactions.value
  return {
    totalTransactions: transactions.length,
    totalSpent: transactions.reduce((sum, t) => sum + t.amount, 0),
    activeShipments: transactions.filter(t => 
      t.delivery_status !== 'delivered' && t.delivery_status !== 'cancelled'
    ).length
  }
})

const getStatusClass = (status: string) => {
  const statusClasses: Record<string, string> = {
    'requested': 'status-requested',
    'paid': 'status-paid',
    'Payment Pending': 'status-pending',
    'delivered': 'status-delivered',
    'processing': 'status-processing',
  }
  return statusClasses[status] || 'status-requested'
}

onMounted(() => {
  transactionsStore.fetchTransactions()
})
</script>
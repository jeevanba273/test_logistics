<template>
  <div class="max-w-2xl mx-auto py-6 sm:px-6 lg:px-8">
    <div class="px-4 py-6 sm:px-0">
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900">Profile</h1>
        <p class="mt-2 text-gray-600">Your account information and activity</p>
      </div>

      <!-- User Information -->
      <div class="card mb-6">
        <h2 class="text-xl font-semibold text-gray-900 mb-4">Account Information</h2>
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-500">Username</label>
            <p class="mt-1 text-sm text-gray-900">{{ authStore.user?.username }}</p>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-500">Email</label>
            <p class="mt-1 text-sm text-gray-900">{{ authStore.user?.email }}</p>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-500">Role</label>
            <span
              class="mt-1 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
              :class="authStore.isAdmin ? 'bg-purple-100 text-purple-800' : 'bg-blue-100 text-blue-800'"
            >
              {{ authStore.user?.role }}
            </span>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-500">Member Since</label>
            <p class="mt-1 text-sm text-gray-900">{{ formatDate(authStore.user?.created_at || '') }}</p>
          </div>
        </div>
      </div>

      <!-- Activity Summary -->
      <div class="card mb-6">
        <h2 class="text-xl font-semibold text-gray-900 mb-4">Activity Summary</h2>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div class="text-center">
            <div class="text-2xl font-bold text-primary-600">{{ userStats.totalTransactions }}</div>
            <div class="text-sm text-gray-500">Total Transactions</div>
          </div>
          <div class="text-center">
            <div class="text-2xl font-bold text-green-600">${{ userStats.totalSpent.toFixed(2) }}</div>
            <div class="text-sm text-gray-500">Total Spent</div>
          </div>
          <div class="text-center">
            <div class="text-2xl font-bold text-blue-600">{{ userStats.activeShipments }}</div>
            <div class="text-sm text-gray-500">Active Shipments</div>
          </div>
          <div class="text-center">
            <div class="text-2xl font-bold text-purple-600">{{ userStats.completedShipments }}</div>
            <div class="text-sm text-gray-500">Completed</div>
          </div>
        </div>
      </div>

      <!-- Recent Transactions -->
      <div class="card">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-xl font-semibold text-gray-900">Recent Transactions</h2>
          <RouterLink to="/transactions" class="text-primary-600 hover:text-primary-500 text-sm font-medium">
            View All
          </RouterLink>
        </div>

        <div v-if="recentTransactions.length === 0" class="text-center py-8">
          <DocumentTextIcon class="mx-auto h-12 w-12 text-gray-400" />
          <h3 class="mt-2 text-sm font-medium text-gray-900">No transactions yet</h3>
          <p class="mt-1 text-sm text-gray-500">Get started by creating your first transaction.</p>
          <div class="mt-4">
            <RouterLink to="/transactions/create" class="btn btn-primary">
              Create Transaction
            </RouterLink>
          </div>
        </div>

        <div v-else class="space-y-3">
          <div
            v-for="transaction in recentTransactions"
            :key="transaction.id"
            class="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors cursor-pointer"
            @click="$router.push(`/transactions/${transaction.id}`)"
          >
            <div>
              <p class="text-sm font-medium text-gray-900">Transaction #{{ transaction.id }}</p>
              <p class="text-xs text-gray-500">{{ formatDate(transaction.created_at) }}</p>
            </div>
            <div class="text-right">
              <p class="text-sm font-medium text-gray-900">${{ transaction.amount.toFixed(2) }}</p>
              <span
                class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium"
                :class="getStatusColor(transaction.status)"
              >
                {{ transaction.status }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { DocumentTextIcon } from '@heroicons/vue/24/outline'
import { useAuthStore } from '@/stores/auth'
import { useTransactionsStore } from '@/stores/transactions'

const authStore = useAuthStore()
const transactionsStore = useTransactionsStore()

const userTransactions = computed(() => {
  return transactionsStore.transactions.filter(t => t.user_id === authStore.user?.id)
})

const recentTransactions = computed(() => {
  return userTransactions.value
    .sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
    .slice(0, 5)
})

const userStats = computed(() => {
  const transactions = userTransactions.value
  const paidTransactions = transactions.filter(t => t.payment_status === 'paid')
  
  return {
    totalTransactions: transactions.length,
    totalSpent: paidTransactions.reduce((sum, t) => sum + t.amount, 0),
    activeShipments: transactions.filter(t => ['pending', 'in_transit'].includes(t.status)).length,
    completedShipments: transactions.filter(t => t.status === 'delivered').length
  }
})

const getStatusColor = (status: string) => {
  switch (status.toLowerCase()) {
    case 'pending':
      return 'bg-yellow-100 text-yellow-800'
    case 'in_transit':
      return 'bg-blue-100 text-blue-800'
    case 'delivered':
      return 'bg-green-100 text-green-800'
    case 'cancelled':
      return 'bg-red-100 text-red-800'
    default:
      return 'bg-gray-100 text-gray-800'
  }
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

onMounted(() => {
  if (transactionsStore.transactions.length === 0) {
    transactionsStore.fetchTransactions()
  }
})
</script>
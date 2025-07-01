<template>
  <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
    <div class="px-4 py-6 sm:px-0">
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900">Admin Dashboard</h1>
        <p class="mt-2 text-gray-600">System overview and management</p>
      </div>

      <!-- Admin Stats Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatsCard
          title="Total Revenue"
          :value="`$${stats.totalRevenue.toFixed(2)}`"
          :icon="CurrencyDollarIcon"
          icon-color="text-green-600"
        />
        <StatsCard
          title="Total Users"
          :value="stats.totalUsers"
          :icon="UsersIcon"
          icon-color="text-blue-600"
        />
        <StatsCard
          title="Active Shipments"
          :value="stats.activeShipments"
          :icon="TruckIcon"
          icon-color="text-purple-600"
        />
        <StatsCard
          title="Completed Orders"
          :value="stats.completedOrders"
          :icon="CheckCircleIcon"
          icon-color="text-green-600"
        />
      </div>

      <!-- Management Actions -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <div class="card">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
          <div class="space-y-3">
            <RouterLink to="/transactions" class="btn btn-primary w-full">
              Manage All Transactions
            </RouterLink>
            <RouterLink to="/transactions/create" class="btn btn-secondary w-full">
              Create New Transaction
            </RouterLink>
          </div>
        </div>

        <div class="card">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">System Status</h3>
          <div class="space-y-3">
            <div class="flex items-center justify-between">
              <span class="text-sm text-gray-600">System Status</span>
              <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                Online
              </span>
            </div>
            <div class="flex items-center justify-between">
              <span class="text-sm text-gray-600">Database</span>
              <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                Connected
              </span>
            </div>
            <div class="flex items-center justify-between">
              <span class="text-sm text-gray-600">Last Backup</span>
              <span class="text-sm text-gray-900">{{ new Date().toLocaleDateString() }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Recent Activity -->
      <div class="card">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-xl font-semibold text-gray-900">Recent Activity</h2>
          <RouterLink to="/transactions" class="btn btn-primary">
            View All Transactions
          </RouterLink>
        </div>

        <div v-if="transactionsStore.loading" class="text-center py-8">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mx-auto"></div>
          <p class="mt-2 text-gray-600">Loading transactions...</p>
        </div>

        <div v-else-if="recentTransactions.length === 0" class="text-center py-8">
          <DocumentTextIcon class="mx-auto h-12 w-12 text-gray-400" />
          <h3 class="mt-2 text-sm font-medium text-gray-900">No recent activity</h3>
          <p class="mt-1 text-sm text-gray-500">Transactions will appear here once created.</p>
        </div>

        <div v-else class="space-y-4">
          <TransactionCard
            v-for="transaction in recentTransactions"
            :key="transaction.id"
            :transaction="transaction"
            @click="$router.push(`/transactions/${transaction.id}`)"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import {
  CurrencyDollarIcon,
  UsersIcon,
  TruckIcon,
  CheckCircleIcon,
  DocumentTextIcon
} from '@heroicons/vue/24/outline'
import { useTransactionsStore } from '@/stores/transactions'
import StatsCard from '@/components/StatsCard.vue'
import TransactionCard from '@/components/TransactionCard.vue'

const transactionsStore = useTransactionsStore()

const recentTransactions = computed(() => {
  return transactionsStore.transactions
    .sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
    .slice(0, 10)
})

const stats = computed(() => {
  const transactions = transactionsStore.transactions
  const paidTransactions = transactions.filter(t => t.payment_status === 'paid')
  
  return {
    totalRevenue: paidTransactions.reduce((sum, t) => sum + t.amount, 0),
    totalUsers: new Set(transactions.map(t => t.user_id)).size,
    activeShipments: transactions.filter(t => ['pending', 'in_transit'].includes(t.status)).length,
    completedOrders: transactions.filter(t => t.status === 'delivered').length
  }
})

onMounted(() => {
  transactionsStore.fetchTransactions()
})
</script>
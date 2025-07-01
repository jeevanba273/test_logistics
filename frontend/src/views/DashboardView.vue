<template>
  <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
    <div class="px-4 py-6 sm:px-0">
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p class="mt-2 text-gray-600">Welcome back, {{ authStore.user?.username }}!</p>
      </div>

      <!-- Stats Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatsCard
          title="Total Transactions"
          :value="stats.totalTransactions"
          :icon="DocumentTextIcon"
          icon-color="text-blue-600"
        />
        <StatsCard
          title="Pending Payments"
          :value="stats.pendingPayments"
          :icon="CreditCardIcon"
          icon-color="text-yellow-600"
        />
        <StatsCard
          title="In Transit"
          :value="stats.inTransit"
          :icon="TruckIcon"
          icon-color="text-purple-600"
        />
        <StatsCard
          title="Delivered"
          :value="stats.delivered"
          :icon="CheckCircleIcon"
          icon-color="text-green-600"
        />
      </div>

      <!-- Recent Transactions -->
      <div class="card">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-xl font-semibold text-gray-900">Recent Transactions</h2>
          <RouterLink to="/transactions" class="btn btn-primary">
            View All
          </RouterLink>
        </div>

        <div v-if="transactionsStore.loading" class="text-center py-8">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mx-auto"></div>
          <p class="mt-2 text-gray-600">Loading transactions...</p>
        </div>

        <div v-else-if="recentTransactions.length === 0" class="text-center py-8">
          <DocumentTextIcon class="mx-auto h-12 w-12 text-gray-400" />
          <h3 class="mt-2 text-sm font-medium text-gray-900">No transactions</h3>
          <p class="mt-1 text-sm text-gray-500">Get started by creating a new transaction.</p>
          <div class="mt-6">
            <RouterLink to="/transactions/create" class="btn btn-primary">
              Create Transaction
            </RouterLink>
          </div>
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
  DocumentTextIcon,
  CreditCardIcon,
  TruckIcon,
  CheckCircleIcon
} from '@heroicons/vue/24/outline'
import { useAuthStore } from '@/stores/auth'
import { useTransactionsStore } from '@/stores/transactions'
import StatsCard from '@/components/StatsCard.vue'
import TransactionCard from '@/components/TransactionCard.vue'

const authStore = useAuthStore()
const transactionsStore = useTransactionsStore()

const recentTransactions = computed(() => {
  return transactionsStore.transactions
    .filter(t => authStore.isAdmin || t.user_id === authStore.user?.id)
    .slice(0, 5)
})

const stats = computed(() => {
  const userTransactions = authStore.isAdmin 
    ? transactionsStore.transactions
    : transactionsStore.transactions.filter(t => t.user_id === authStore.user?.id)

  return {
    totalTransactions: userTransactions.length,
    pendingPayments: userTransactions.filter(t => t.payment_status === 'pending').length,
    inTransit: userTransactions.filter(t => t.status === 'in_transit').length,
    delivered: userTransactions.filter(t => t.status === 'delivered').length
  }
})

onMounted(() => {
  transactionsStore.fetchTransactions()
})
</script>
<template>
  <div class="p-6 space-y-6">
    <!-- Header -->
    <div class="animate-fade-in">
      <h1 class="text-3xl font-bold text-gray-900">Dashboard</h1>
      <p class="text-gray-600 mt-1">Welcome back, {{ authStore.user?.username }}!</p>
    </div>

    <!-- Stats Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <StatsCard
        title="Total Transactions"
        :value="stats.total"
        :icon="DocumentTextIcon"
        color="blue"
      />
      <StatsCard
        title="Pending Payments"
        :value="stats.pendingPayments"
        :icon="CreditCardIcon"
        color="yellow"
      />
      <StatsCard
        title="In Transit"
        :value="stats.inTransit"
        :icon="TruckIcon"
        color="purple"
      />
      <StatsCard
        title="Delivered"
        :value="stats.delivered"
        :icon="CheckCircleIcon"
        color="green"
      />
    </div>

    <!-- Recent Transactions -->
    <div class="animate-slide-up">
      <div class="flex items-center justify-between mb-6">
        <h2 class="text-xl font-semibold text-gray-900">Recent Transactions</h2>
        <router-link
          to="/transactions"
          class="text-primary-600 hover:text-primary-700 font-medium text-sm"
        >
          View all →
        </router-link>
      </div>

      <div v-if="transactionsStore.isLoading" class="flex justify-center py-12">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
      </div>

      <div v-else-if="recentTransactions.length === 0" class="text-center py-12">
        <DocumentTextIcon class="w-12 h-12 text-gray-400 mx-auto mb-4" />
        <p class="text-gray-500">No transactions found</p>
        <router-link
          to="/transactions/create"
          class="btn-primary mt-4 inline-flex items-center"
        >
          <PlusIcon class="w-4 h-4 mr-2" />
          Create Transaction
        </router-link>
      </div>

      <div v-else class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <TransactionCard
          v-for="transaction in recentTransactions"
          :key="transaction.id"
          :transaction="transaction"
          @view="viewTransaction"
          @pay="payTransaction"
        />
      </div>
    </div>

    <!-- Quick Actions -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 animate-fade-in">
      <div class="card text-center">
        <PlusIcon class="w-8 h-8 text-primary-600 mx-auto mb-3" />
        <h3 class="text-lg font-medium text-gray-900 mb-2">Create Transaction</h3>
        <p class="text-gray-600 text-sm mb-4">Start a new shipment request</p>
        <router-link to="/transactions/create" class="btn-primary">
          Get Started
        </router-link>
      </div>

      <div class="card text-center">
        <DocumentTextIcon class="w-8 h-8 text-green-600 mx-auto mb-3" />
        <h3 class="text-lg font-medium text-gray-900 mb-2">View Transactions</h3>
        <p class="text-gray-600 text-sm mb-4">Track all your shipments</p>
        <router-link to="/transactions" class="btn-secondary">
          View All
        </router-link>
      </div>

      <div v-if="authStore.isAdmin" class="card text-center">
        <ChartBarIcon class="w-8 h-8 text-purple-600 mx-auto mb-3" />
        <h3 class="text-lg font-medium text-gray-900 mb-2">Admin Panel</h3>
        <p class="text-gray-600 text-sm mb-4">Manage system operations</p>
        <router-link to="/admin" class="btn-secondary">
          Open Panel
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useTransactionsStore } from '@/stores/transactions'
import { useToast } from 'vue-toastification'
import StatsCard from '@/components/StatsCard.vue'
import TransactionCard from '@/components/TransactionCard.vue'
import {
  DocumentTextIcon,
  CreditCardIcon,
  TruckIcon,
  CheckCircleIcon,
  PlusIcon,
  ChartBarIcon
} from '@heroicons/vue/24/outline'

const router = useRouter()
const authStore = useAuthStore()
const transactionsStore = useTransactionsStore()
const toast = useToast()

const recentTransactions = computed(() => 
  transactionsStore.transactions.slice(0, 6)
)

const stats = computed(() => {
  const transactions = transactionsStore.transactions
  return {
    total: transactions.length,
    pendingPayments: transactions.filter(t => t.internal_status === 'Payment Pending').length,
    inTransit: transactions.filter(t => t.delivery_status === 'processing').length,
    delivered: transactions.filter(t => t.delivery_status === 'delivered').length,
  }
})

const viewTransaction = (id: number) => {
  router.push(`/transactions/${id}`)
}

const payTransaction = async (id: number) => {
  try {
    await transactionsStore.payTransaction(id)
    toast.success('Payment processed successfully!')
  } catch (error: any) {
    toast.error(error.response?.data?.message || 'Payment failed')
  }
}

onMounted(() => {
  transactionsStore.fetchTransactions()
})
</script>
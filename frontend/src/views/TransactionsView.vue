<template>
  <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
    <div class="px-4 py-6 sm:px-0">
      <div class="flex items-center justify-between mb-8">
        <div>
          <h1 class="text-3xl font-bold text-gray-900">Transactions</h1>
          <p class="mt-2 text-gray-600">Manage your shipment transactions</p>
        </div>
        <RouterLink to="/transactions/create" class="btn btn-primary">
          Create Transaction
        </RouterLink>
      </div>

      <!-- Filters -->
      <div class="card mb-6">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Status</label>
            <select v-model="filters.status" class="input">
              <option value="">All Statuses</option>
              <option value="pending">Pending</option>
              <option value="in_transit">In Transit</option>
              <option value="delivered">Delivered</option>
              <option value="cancelled">Cancelled</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Payment Status</label>
            <select v-model="filters.paymentStatus" class="input">
              <option value="">All Payment Statuses</option>
              <option value="pending">Pending</option>
              <option value="paid">Paid</option>
              <option value="failed">Failed</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Search</label>
            <input
              v-model="filters.search"
              type="text"
              placeholder="Search transactions..."
              class="input"
            />
          </div>
        </div>
      </div>

      <!-- Transactions List -->
      <div v-if="transactionsStore.loading" class="text-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
        <p class="mt-4 text-gray-600">Loading transactions...</p>
      </div>

      <div v-else-if="filteredTransactions.length === 0" class="text-center py-12">
        <DocumentTextIcon class="mx-auto h-16 w-16 text-gray-400" />
        <h3 class="mt-4 text-lg font-medium text-gray-900">No transactions found</h3>
        <p class="mt-2 text-gray-500">
          {{ transactionsStore.transactions.length === 0 
            ? 'Get started by creating your first transaction.' 
            : 'Try adjusting your filters or search terms.' 
          }}
        </p>
        <div class="mt-6">
          <RouterLink to="/transactions/create" class="btn btn-primary">
            Create Transaction
          </RouterLink>
        </div>
      </div>

      <div v-else class="space-y-4">
        <TransactionCard
          v-for="transaction in filteredTransactions"
          :key="transaction.id"
          :transaction="transaction"
          @click="$router.push(`/transactions/${transaction.id}`)"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive } from 'vue'
import { RouterLink } from 'vue-router'
import { DocumentTextIcon } from '@heroicons/vue/24/outline'
import { useAuthStore } from '@/stores/auth'
import { useTransactionsStore } from '@/stores/transactions'
import TransactionCard from '@/components/TransactionCard.vue'

const authStore = useAuthStore()
const transactionsStore = useTransactionsStore()

const filters = reactive({
  status: '',
  paymentStatus: '',
  search: ''
})

const filteredTransactions = computed(() => {
  let transactions = transactionsStore.transactions

  // Filter by user if not admin
  if (!authStore.isAdmin) {
    transactions = transactions.filter(t => t.user_id === authStore.user?.id)
  }

  // Apply filters
  if (filters.status) {
    transactions = transactions.filter(t => t.status === filters.status)
  }

  if (filters.paymentStatus) {
    transactions = transactions.filter(t => t.payment_status === filters.paymentStatus)
  }

  if (filters.search) {
    const search = filters.search.toLowerCase()
    transactions = transactions.filter(t => 
      t.id.toString().includes(search) ||
      t.amount.toString().includes(search) ||
      (t.user?.username && t.user.username.toLowerCase().includes(search))
    )
  }

  return transactions.sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
})

onMounted(() => {
  transactionsStore.fetchTransactions()
})
</script>
<template>
  <div class="p-6 space-y-6">
    <!-- Header -->
    <div class="flex items-center justify-between animate-fade-in">
      <div>
        <h1 class="text-3xl font-bold text-gray-900">Transactions</h1>
        <p class="text-gray-600 mt-1">Manage all your shipments</p>
      </div>
      <router-link to="/transactions/create" class="btn-primary">
        <PlusIcon class="w-4 h-4 mr-2" />
        New Transaction
      </router-link>
    </div>

    <!-- Filters -->
    <div class="card animate-slide-up">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Status</label>
          <select v-model="filters.status" class="input-field">
            <option value="">All Status</option>
            <option value="requested">Requested</option>
            <option value="Payment Pending">Payment Pending</option>
            <option value="paid">Paid</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Type</label>
          <select v-model="filters.type" class="input-field">
            <option value="">All Types</option>
            <option value="edible">Edible</option>
            <option value="fragile">Fragile</option>
            <option value="non-fragile">Non-fragile</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Search</label>
          <input
            v-model="filters.search"
            type="text"
            placeholder="Search transactions..."
            class="input-field"
          />
        </div>
        <div class="flex items-end">
          <button @click="clearFilters" class="btn-secondary w-full">
            Clear Filters
          </button>
        </div>
      </div>
    </div>

    <!-- Transactions Grid -->
    <div v-if="transactionsStore.isLoading" class="flex justify-center py-12">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
    </div>

    <div v-else-if="filteredTransactions.length === 0" class="text-center py-12 animate-fade-in">
      <DocumentTextIcon class="w-12 h-12 text-gray-400 mx-auto mb-4" />
      <p class="text-gray-500 mb-4">No transactions found</p>
      <router-link to="/transactions/create" class="btn-primary">
        <PlusIcon class="w-4 h-4 mr-2" />
        Create Your First Transaction
      </router-link>
    </div>

    <div v-else class="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
      <TransactionCard
        v-for="transaction in filteredTransactions"
        :key="transaction.id"
        :transaction="transaction"
        @view="viewTransaction"
        @pay="payTransaction"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useTransactionsStore } from '@/stores/transactions'
import { useToast } from 'vue-toastification'
import TransactionCard from '@/components/TransactionCard.vue'
import { DocumentTextIcon, PlusIcon } from '@heroicons/vue/24/outline'

const router = useRouter()
const transactionsStore = useTransactionsStore()
const toast = useToast()

const filters = reactive({
  status: '',
  type: '',
  search: ''
})

const filteredTransactions = computed(() => {
  let transactions = transactionsStore.transactions

  if (filters.status) {
    transactions = transactions.filter(t => t.internal_status === filters.status)
  }

  if (filters.type) {
    transactions = transactions.filter(t => t.type === filters.type)
  }

  if (filters.search) {
    const search = filters.search.toLowerCase()
    transactions = transactions.filter(t =>
      t.name.toLowerCase().includes(search) ||
      t.source_city.toLowerCase().includes(search) ||
      t.destination_city.toLowerCase().includes(search) ||
      t.user.toLowerCase().includes(search)
    )
  }

  return transactions
})

const clearFilters = () => {
  filters.status = ''
  filters.type = ''
  filters.search = ''
}

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
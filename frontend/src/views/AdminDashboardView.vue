<template>
  <div class="p-6 space-y-6">
    <!-- Header -->
    <div class="animate-fade-in">
      <h1 class="text-3xl font-bold text-gray-900">Admin Dashboard</h1>
      <p class="text-gray-600 mt-1">System overview and management</p>
    </div>

    <!-- Stats Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <StatsCard
        title="Total Users"
        :value="stats.totalUsers"
        :icon="UsersIcon"
        color="blue"
      />
      <StatsCard
        title="Total Transactions"
        :value="stats.totalTransactions"
        :icon="DocumentTextIcon"
        color="green"
      />
      <StatsCard
        title="Revenue"
        :value="`$${stats.totalRevenue.toLocaleString()}`"
        :icon="CurrencyDollarIcon"
        color="purple"
      />
      <StatsCard
        title="Pending Actions"
        :value="stats.pendingActions"
        :icon="ExclamationTriangleIcon"
        color="yellow"
      />
    </div>

    <!-- Recent Transactions Table -->
    <div class="card animate-slide-up">
      <div class="flex items-center justify-between mb-6">
        <h2 class="text-xl font-semibold text-gray-900">Recent Transactions</h2>
        <div class="flex space-x-2">
          <select v-model="statusFilter" class="input-field">
            <option value="">All Status</option>
            <option value="requested">Requested</option>
            <option value="Payment Pending">Payment Pending</option>
            <option value="paid">Paid</option>
          </select>
        </div>
      </div>

      <div v-if="transactionsStore.isLoading" class="flex justify-center py-8">
        <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-primary-600"></div>
      </div>

      <div v-else class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Transaction
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                User
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Route
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Amount
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Status
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="transaction in filteredTransactions" :key="transaction.id" class="hover:bg-gray-50">
              <td class="px-6 py-4 whitespace-nowrap">
                <div>
                  <div class="text-sm font-medium text-gray-900">{{ transaction.name }}</div>
                  <div class="text-sm text-gray-500">{{ transaction.type }}</div>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm text-gray-900">{{ transaction.user }}</div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm text-gray-900">
                  {{ transaction.source_city }} → {{ transaction.destination_city }}
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm font-medium text-gray-900">${{ transaction.amount.toLocaleString() }}</div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex space-x-1">
                  <span :class="getStatusClass(transaction.internal_status)" class="status-badge">
                    {{ transaction.internal_status }}
                  </span>
                  <span :class="getStatusClass(transaction.delivery_status)" class="status-badge">
                    {{ transaction.delivery_status }}
                  </span>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                <div class="flex space-x-2">
                  <button
                    @click="viewTransaction(transaction.id)"
                    class="text-primary-600 hover:text-primary-900"
                  >
                    View
                  </button>
                  <button
                    v-if="transaction.internal_status === 'requested'"
                    @click="showUpdateAmountModal(transaction)"
                    class="text-green-600 hover:text-green-900"
                  >
                    Set Amount
                  </button>
                  <button
                    v-if="transaction.internal_status === 'paid'"
                    @click="showUpdateDeliveryModal(transaction)"
                    class="text-blue-600 hover:text-blue-900"
                  >
                    Update Delivery
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Update Amount Modal -->
    <div v-if="showAmountModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
        <div class="mt-3">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Update Amount</h3>
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-2">Amount</label>
            <input
              v-model="modalData.amount"
              type="number"
              class="input-field"
              placeholder="Enter amount"
            />
          </div>
          <div class="flex justify-end space-x-3">
            <button @click="closeModal" class="btn-secondary">Cancel</button>
            <button @click="updateAmount" class="btn-primary">Update</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Update Delivery Modal -->
    <div v-if="showDeliveryModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
        <div class="mt-3">
          <h3 class="text-lg font-medium text-gray-900 mb-4">Update Delivery</h3>
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Delivery Date</label>
              <input
                v-model="modalData.deliveryDate"
                type="date"
                class="input-field"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Delivery Status</label>
              <select v-model="modalData.deliveryStatus" class="input-field">
                <option value="processing">Processing</option>
                <option value="in transit">In Transit</option>
                <option value="delivered">Delivered</option>
              </select>
            </div>
          </div>
          <div class="flex justify-end space-x-3 mt-6">
            <button @click="closeModal" class="btn-secondary">Cancel</button>
            <button @click="updateDelivery" class="btn-primary">Update</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useTransactionsStore } from '@/stores/transactions'
import { useToast } from 'vue-toastification'
import StatsCard from '@/components/StatsCard.vue'
import type { Transaction } from '@/stores/transactions'
import {
  UsersIcon,
  DocumentTextIcon,
  CurrencyDollarIcon,
  ExclamationTriangleIcon
} from '@heroicons/vue/24/outline'

const router = useRouter()
const transactionsStore = useTransactionsStore()
const toast = useToast()

const statusFilter = ref('')
const showAmountModal = ref(false)
const showDeliveryModal = ref(false)
const selectedTransaction = ref<Transaction | null>(null)

const modalData = reactive({
  amount: '',
  deliveryDate: '',
  deliveryStatus: 'processing'
})

const filteredTransactions = computed(() => {
  let transactions = transactionsStore.transactions
  if (statusFilter.value) {
    transactions = transactions.filter(t => t.internal_status === statusFilter.value)
  }
  return transactions.slice(0, 20) // Show latest 20
})

const stats = computed(() => {
  const transactions = transactionsStore.transactions
  return {
    totalUsers: new Set(transactions.map(t => t.user_id)).size,
    totalTransactions: transactions.length,
    totalRevenue: transactions.reduce((sum, t) => sum + t.amount, 0),
    pendingActions: transactions.filter(t => 
      t.internal_status === 'requested' || t.internal_status === 'Payment Pending'
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

const viewTransaction = (id: number) => {
  router.push(`/transactions/${id}`)
}

const showUpdateAmountModal = (transaction: Transaction) => {
  selectedTransaction.value = transaction
  modalData.amount = transaction.amount.toString()
  showAmountModal.value = true
}

const showUpdateDeliveryModal = (transaction: Transaction) => {
  selectedTransaction.value = transaction
  modalData.deliveryDate = ''
  modalData.deliveryStatus = transaction.delivery_status
  showDeliveryModal.value = true
}

const closeModal = () => {
  showAmountModal.value = false
  showDeliveryModal.value = false
  selectedTransaction.value = null
  modalData.amount = ''
  modalData.deliveryDate = ''
  modalData.deliveryStatus = 'processing'
}

const updateAmount = async () => {
  if (!selectedTransaction.value || !modalData.amount) return
  
  try {
    await transactionsStore.updateAmount(selectedTransaction.value.id, parseFloat(modalData.amount))
    toast.success('Amount updated successfully!')
    closeModal()
  } catch (error: any) {
    toast.error(error.response?.data?.message || 'Failed to update amount')
  }
}

const updateDelivery = async () => {
  if (!selectedTransaction.value) return
  
  try {
    if (modalData.deliveryDate) {
      await transactionsStore.updateDeliveryDate(selectedTransaction.value.id, modalData.deliveryDate)
    }
    if (modalData.deliveryStatus) {
      await transactionsStore.updateDeliveryStatus(selectedTransaction.value.id, modalData.deliveryStatus)
    }
    toast.success('Delivery information updated successfully!')
    closeModal()
  } catch (error: any) {
    toast.error(error.response?.data?.message || 'Failed to update delivery information')
  }
}

onMounted(() => {
  transactionsStore.fetchTransactions()
})
</script>
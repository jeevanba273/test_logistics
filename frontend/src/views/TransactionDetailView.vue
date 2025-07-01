<template>
  <div class="max-w-4xl mx-auto py-6 sm:px-6 lg:px-8">
    <div class="px-4 py-6 sm:px-0">
      <div class="flex items-center justify-between mb-8">
        <div>
          <h1 class="text-3xl font-bold text-gray-900">Transaction #{{ $route.params.id }}</h1>
          <p class="mt-2 text-gray-600">Transaction details and management</p>
        </div>
        <RouterLink to="/transactions" class="btn btn-secondary">
          Back to Transactions
        </RouterLink>
      </div>

      <div v-if="loading" class="text-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
        <p class="mt-4 text-gray-600">Loading transaction...</p>
      </div>

      <div v-else-if="!transaction" class="text-center py-12">
        <DocumentTextIcon class="mx-auto h-16 w-16 text-gray-400" />
        <h3 class="mt-4 text-lg font-medium text-gray-900">Transaction not found</h3>
        <p class="mt-2 text-gray-500">The transaction you're looking for doesn't exist.</p>
      </div>

      <div v-else class="space-y-6">
        <!-- Transaction Info -->
        <div class="card">
          <h2 class="text-xl font-semibold text-gray-900 mb-4">Transaction Information</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h3 class="text-sm font-medium text-gray-500">Amount</h3>
              <p class="mt-1 text-lg font-semibold text-gray-900">${{ transaction.amount.toFixed(2) }}</p>
            </div>
            <div>
              <h3 class="text-sm font-medium text-gray-500">Status</h3>
              <span
                class="mt-1 inline-flex items-center px-2.5 py-0.5 rounded-full text-sm font-medium"
                :class="getStatusColor(transaction.status)"
              >
                {{ transaction.status }}
              </span>
            </div>
            <div>
              <h3 class="text-sm font-medium text-gray-500">Payment Status</h3>
              <span
                class="mt-1 inline-flex items-center px-2.5 py-0.5 rounded-full text-sm font-medium"
                :class="getPaymentStatusColor(transaction.payment_status)"
              >
                {{ transaction.payment_status }}
              </span>
            </div>
            <div>
              <h3 class="text-sm font-medium text-gray-500">Delivery Date</h3>
              <p class="mt-1 text-sm text-gray-900">{{ formatDate(transaction.delivery_date) }}</p>
            </div>
            <div>
              <h3 class="text-sm font-medium text-gray-500">Created</h3>
              <p class="mt-1 text-sm text-gray-900">{{ formatDate(transaction.created_at) }}</p>
            </div>
            <div>
              <h3 class="text-sm font-medium text-gray-500">Last Updated</h3>
              <p class="mt-1 text-sm text-gray-900">{{ formatDate(transaction.updated_at) }}</p>
            </div>
          </div>
        </div>

        <!-- User Actions -->
        <div v-if="!authStore.isAdmin" class="card">
          <h2 class="text-xl font-semibold text-gray-900 mb-4">Actions</h2>
          <div class="flex space-x-4">
            <button
              v-if="transaction.payment_status === 'pending'"
              @click="handlePayment"
              :disabled="transactionsStore.loading"
              class="btn btn-primary"
            >
              <span v-if="transactionsStore.loading">Processing...</span>
              <span v-else>Pay Now</span>
            </button>
            <button
              v-if="['pending', 'in_transit'].includes(transaction.status)"
              @click="showDeleteConfirm = true"
              class="btn btn-danger"
            >
              Cancel Transaction
            </button>
          </div>
        </div>

        <!-- Admin Actions -->
        <div v-if="authStore.isAdmin" class="card">
          <h2 class="text-xl font-semibold text-gray-900 mb-4">Admin Actions</h2>
          
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Update Amount</label>
              <div class="flex">
                <input
                  v-model.number="adminForm.amount"
                  type="number"
                  step="0.01"
                  min="0"
                  class="input flex-1"
                  placeholder="New amount"
                />
                <button
                  @click="handleUpdateAmount"
                  :disabled="transactionsStore.loading"
                  class="btn btn-primary ml-2"
                >
                  Update
                </button>
              </div>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Update Status</label>
              <div class="flex">
                <select v-model="adminForm.status" class="input flex-1">
                  <option value="pending">Pending</option>
                  <option value="in_transit">In Transit</option>
                  <option value="delivered">Delivered</option>
                  <option value="cancelled">Cancelled</option>
                </select>
                <button
                  @click="handleUpdateStatus"
                  :disabled="transactionsStore.loading"
                  class="btn btn-primary ml-2"
                >
                  Update
                </button>
              </div>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Update Delivery Date</label>
              <div class="flex">
                <input
                  v-model="adminForm.delivery_date"
                  type="date"
                  class="input flex-1"
                />
                <button
                  @click="handleUpdateDeliveryDate"
                  :disabled="transactionsStore.loading"
                  class="btn btn-primary ml-2"
                >
                  Update
                </button>
              </div>
            </div>
          </div>

          <div class="pt-4 border-t border-gray-200">
            <button
              @click="showDeleteConfirm = true"
              class="btn btn-danger"
            >
              Delete Transaction
            </button>
          </div>
        </div>
      </div>

      <!-- Delete Confirmation Modal -->
      <div
        v-if="showDeleteConfirm"
        class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50"
        @click="showDeleteConfirm = false"
      >
        <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white" @click.stop>
          <div class="mt-3 text-center">
            <h3 class="text-lg font-medium text-gray-900">Confirm Deletion</h3>
            <div class="mt-2 px-7 py-3">
              <p class="text-sm text-gray-500">
                Are you sure you want to delete this transaction? This action cannot be undone.
              </p>
            </div>
            <div class="flex justify-center space-x-4 mt-4">
              <button
                @click="showDeleteConfirm = false"
                class="btn btn-secondary"
              >
                Cancel
              </button>
              <button
                @click="handleDelete"
                :disabled="transactionsStore.loading"
                class="btn btn-danger"
              >
                <span v-if="transactionsStore.loading">Deleting...</span>
                <span v-else>Delete</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'
import { DocumentTextIcon } from '@heroicons/vue/24/outline'
import { useAuthStore } from '@/stores/auth'
import { useTransactionsStore } from '@/stores/transactions'

const authStore = useAuthStore()
const transactionsStore = useTransactionsStore()
const route = useRoute()
const router = useRouter()

const loading = ref(false)
const showDeleteConfirm = ref(false)

const adminForm = reactive({
  amount: 0,
  status: '',
  delivery_date: ''
})

const transaction = computed(() => {
  const id = parseInt(route.params.id as string)
  return transactionsStore.transactions.find(t => t.id === id)
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

const getPaymentStatusColor = (status: string) => {
  switch (status.toLowerCase()) {
    case 'paid':
      return 'bg-green-100 text-green-800'
    case 'pending':
      return 'bg-yellow-100 text-yellow-800'
    case 'failed':
      return 'bg-red-100 text-red-800'
    default:
      return 'bg-gray-100 text-gray-800'
  }
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const handlePayment = async () => {
  if (!transaction.value) return
  
  const success = await transactionsStore.payTransaction(transaction.value.id)
  if (success) {
    await transactionsStore.fetchTransactions()
  }
}

const handleUpdateAmount = async () => {
  if (!transaction.value || !adminForm.amount) return
  
  const success = await transactionsStore.updateAmount(transaction.value.id, adminForm.amount)
  if (success) {
    adminForm.amount = 0
  }
}

const handleUpdateStatus = async () => {
  if (!transaction.value || !adminForm.status) return
  
  const success = await transactionsStore.updateDeliveryStatus(transaction.value.id, adminForm.status)
  if (success) {
    adminForm.status = ''
  }
}

const handleUpdateDeliveryDate = async () => {
  if (!transaction.value || !adminForm.delivery_date) return
  
  const success = await transactionsStore.updateDeliveryDate(transaction.value.id, adminForm.delivery_date)
  if (success) {
    adminForm.delivery_date = ''
  }
}

const handleDelete = async () => {
  if (!transaction.value) return
  
  const success = await transactionsStore.deleteTransaction(transaction.value.id)
  if (success) {
    router.push('/transactions')
  }
  showDeleteConfirm.value = false
}

onMounted(async () => {
  if (transactionsStore.transactions.length === 0) {
    await transactionsStore.fetchTransactions()
  }
  
  if (transaction.value) {
    adminForm.amount = transaction.value.amount
    adminForm.status = transaction.value.status
    adminForm.delivery_date = transaction.value.delivery_date.split('T')[0]
  }
})
</script>
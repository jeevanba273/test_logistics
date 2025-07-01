<template>
  <div class="p-6 max-w-4xl mx-auto">
    <div v-if="isLoading" class="flex justify-center py-12">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
    </div>

    <div v-else-if="transaction" class="space-y-6">
      <!-- Header -->
      <div class="flex items-center justify-between animate-fade-in">
        <div>
          <h1 class="text-3xl font-bold text-gray-900">{{ transaction.name }}</h1>
          <p class="text-gray-600 mt-1">Transaction #{{ transaction.id }}</p>
        </div>
        <div class="flex space-x-3">
          <span :class="getStatusClass(transaction.internal_status)" class="status-badge">
            {{ transaction.internal_status }}
          </span>
          <span :class="getStatusClass(transaction.delivery_status)" class="status-badge">
            {{ transaction.delivery_status }}
          </span>
        </div>
      </div>

      <!-- Main Content -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Transaction Details -->
        <div class="lg:col-span-2 space-y-6">
          <div class="card animate-slide-up">
            <h2 class="text-lg font-semibold text-gray-900 mb-4">Shipment Information</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <p class="text-sm text-gray-500 uppercase tracking-wide">Type</p>
                <p class="text-base font-medium text-gray-900">{{ transaction.type }}</p>
              </div>
              <div>
                <p class="text-sm text-gray-500 uppercase tracking-wide">Date Created</p>
                <p class="text-base font-medium text-gray-900">{{ formatDate(transaction.date) }}</p>
              </div>
              <div>
                <p class="text-sm text-gray-500 uppercase tracking-wide">Source City</p>
                <p class="text-base font-medium text-gray-900">{{ transaction.source_city }}</p>
              </div>
              <div>
                <p class="text-sm text-gray-500 uppercase tracking-wide">Destination City</p>
                <p class="text-base font-medium text-gray-900">{{ transaction.destination_city }}</p>
              </div>
              <div>
                <p class="text-sm text-gray-500 uppercase tracking-wide">Delivery Date</p>
                <p class="text-base font-medium text-gray-900">
                  {{ transaction.delivery_date !== 'to be updated' ? formatDate(transaction.delivery_date) : 'To be updated' }}
                </p>
              </div>
              <div>
                <p class="text-sm text-gray-500 uppercase tracking-wide">Created By</p>
                <p class="text-base font-medium text-gray-900">{{ transaction.user }}</p>
              </div>
            </div>
            <div v-if="transaction.description" class="mt-4">
              <p class="text-sm text-gray-500 uppercase tracking-wide">Description</p>
              <p class="text-base text-gray-900 mt-1">{{ transaction.description }}</p>
            </div>
          </div>

          <!-- Admin Actions -->
          <div v-if="authStore.isAdmin" class="card animate-slide-up">
            <h2 class="text-lg font-semibold text-gray-900 mb-4">Admin Actions</h2>
            <div class="space-y-4">
              <div class="flex items-center space-x-4">
                <input
                  v-model="adminActions.amount"
                  type="number"
                  placeholder="Update amount"
                  class="input-field flex-1"
                />
                <button
                  @click="updateAmount"
                  :disabled="!adminActions.amount"
                  class="btn-primary disabled:opacity-50"
                >
                  Update Amount
                </button>
              </div>
              
              <div class="flex items-center space-x-4">
                <input
                  v-model="adminActions.deliveryDate"
                  type="date"
                  class="input-field flex-1"
                />
                <button
                  @click="updateDeliveryDate"
                  :disabled="!adminActions.deliveryDate"
                  class="btn-primary disabled:opacity-50"
                >
                  Update Delivery Date
                </button>
              </div>
              
              <div class="flex items-center space-x-4">
                <select v-model="adminActions.deliveryStatus" class="input-field flex-1">
                  <option value="">Select delivery status</option>
                  <option value="processing">Processing</option>
                  <option value="in transit">In Transit</option>
                  <option value="delivered">Delivered</option>
                  <option value="cancelled">Cancelled</option>
                </select>
                <button
                  @click="updateDeliveryStatus"
                  :disabled="!adminActions.deliveryStatus"
                  class="btn-primary disabled:opacity-50"
                >
                  Update Status
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Sidebar -->
        <div class="space-y-6">
          <!-- Amount Card -->
          <div class="card animate-bounce-in">
            <h3 class="text-lg font-semibold text-gray-900 mb-2">Amount</h3>
            <p class="text-3xl font-bold text-primary-600">${{ transaction.amount.toLocaleString() }}</p>
            <button
              v-if="canPay"
              @click="payTransaction"
              class="btn-primary w-full mt-4"
            >
              Pay Now
            </button>
          </div>

          <!-- Actions -->
          <div class="card">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">Actions</h3>
            <div class="space-y-3">
              <router-link to="/transactions" class="btn-secondary w-full text-center block">
                Back to Transactions
              </router-link>
              <button
                v-if="canEdit"
                @click="editTransaction"
                class="btn-secondary w-full"
              >
                Edit Transaction
              </button>
              <button
                v-if="canDelete"
                @click="deleteTransaction"
                class="btn-danger w-full"
              >
                Delete Transaction
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="text-center py-12 animate-fade-in">
      <p class="text-gray-500">Transaction not found</p>
      <router-link to="/transactions" class="btn-primary mt-4">
        Back to Transactions
      </router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useTransactionsStore } from '@/stores/transactions'
import { useToast } from 'vue-toastification'
import { format } from 'date-fns'
import type { Transaction } from '@/stores/transactions'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const transactionsStore = useTransactionsStore()
const toast = useToast()

const transaction = ref<Transaction | null>(null)
const isLoading = ref(true)

const adminActions = reactive({
  amount: '',
  deliveryDate: '',
  deliveryStatus: ''
})

const canPay = computed(() => {
  return transaction.value?.internal_status === 'Payment Pending' && 
         (authStore.user?.id === transaction.value?.user_id || authStore.isAdmin)
})

const canEdit = computed(() => {
  return authStore.user?.id === transaction.value?.user_id || authStore.isAdmin
})

const canDelete = computed(() => {
  return authStore.user?.id === transaction.value?.user_id || authStore.isAdmin
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

const formatDate = (dateString: string) => {
  try {
    return format(new Date(dateString), 'MMM dd, yyyy')
  } catch {
    return dateString
  }
}

const payTransaction = async () => {
  if (!transaction.value) return
  
  try {
    await transactionsStore.payTransaction(transaction.value.id)
    toast.success('Payment processed successfully!')
    await fetchTransaction()
  } catch (error: any) {
    toast.error(error.response?.data?.message || 'Payment failed')
  }
}

const updateAmount = async () => {
  if (!transaction.value || !adminActions.amount) return
  
  try {
    await transactionsStore.updateAmount(transaction.value.id, parseFloat(adminActions.amount))
    toast.success('Amount updated successfully!')
    adminActions.amount = ''
    await fetchTransaction()
  } catch (error: any) {
    toast.error(error.response?.data?.message || 'Failed to update amount')
  }
}

const updateDeliveryDate = async () => {
  if (!transaction.value || !adminActions.deliveryDate) return
  
  try {
    await transactionsStore.updateDeliveryDate(transaction.value.id, adminActions.deliveryDate)
    toast.success('Delivery date updated successfully!')
    adminActions.deliveryDate = ''
    await fetchTransaction()
  } catch (error: any) {
    toast.error(error.response?.data?.message || 'Failed to update delivery date')
  }
}

const updateDeliveryStatus = async () => {
  if (!transaction.value || !adminActions.deliveryStatus) return
  
  try {
    await transactionsStore.updateDeliveryStatus(transaction.value.id, adminActions.deliveryStatus)
    toast.success('Delivery status updated successfully!')
    adminActions.deliveryStatus = ''
    await fetchTransaction()
  } catch (error: any) {
    toast.error(error.response?.data?.message || 'Failed to update delivery status')
  }
}

const editTransaction = () => {
  // TODO: Implement edit functionality
  toast.info('Edit functionality coming soon!')
}

const deleteTransaction = async () => {
  if (!transaction.value) return
  
  if (confirm('Are you sure you want to delete this transaction?')) {
    try {
      await transactionsStore.deleteTransaction(transaction.value.id)
      toast.success('Transaction deleted successfully!')
      router.push('/transactions')
    } catch (error: any) {
      toast.error(error.response?.data?.message || 'Failed to delete transaction')
    }
  }
}

const fetchTransaction = async () => {
  const id = parseInt(route.params.id as string)
  if (isNaN(id)) {
    router.push('/transactions')
    return
  }

  try {
    transaction.value = await transactionsStore.getTransactionById(id)
  } catch (error: any) {
    toast.error('Transaction not found')
    router.push('/transactions')
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  fetchTransaction()
})
</script>
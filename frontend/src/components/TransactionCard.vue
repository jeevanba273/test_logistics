<template>
  <div class="card hover:shadow-md transition-shadow duration-200 animate-fade-in">
    <div class="flex items-start justify-between mb-4">
      <div>
        <h3 class="text-lg font-semibold text-gray-900 mb-1">{{ transaction.name }}</h3>
        <p class="text-sm text-gray-500">{{ transaction.type }}</p>
      </div>
      <div class="flex space-x-2">
        <span :class="getStatusClass(transaction.internal_status)" class="status-badge">
          {{ transaction.internal_status }}
        </span>
        <span :class="getStatusClass(transaction.delivery_status)" class="status-badge">
          {{ transaction.delivery_status }}
        </span>
      </div>
    </div>

    <div class="grid grid-cols-2 gap-4 mb-4">
      <div>
        <p class="text-xs text-gray-500 uppercase tracking-wide">From</p>
        <p class="text-sm font-medium text-gray-900">{{ transaction.source_city }}</p>
      </div>
      <div>
        <p class="text-xs text-gray-500 uppercase tracking-wide">To</p>
        <p class="text-sm font-medium text-gray-900">{{ transaction.destination_city }}</p>
      </div>
    </div>

    <div class="flex items-center justify-between mb-4">
      <div>
        <p class="text-xs text-gray-500 uppercase tracking-wide">Amount</p>
        <p class="text-lg font-bold text-primary-600">${{ transaction.amount.toLocaleString() }}</p>
      </div>
      <div class="text-right">
        <p class="text-xs text-gray-500 uppercase tracking-wide">Date</p>
        <p class="text-sm font-medium text-gray-900">{{ formatDate(transaction.date) }}</p>
      </div>
    </div>

    <div class="flex items-center justify-between pt-4 border-t border-gray-200">
      <div class="flex items-center space-x-2">
        <UserIcon class="w-4 h-4 text-gray-400" />
        <span class="text-sm text-gray-600">{{ transaction.user }}</span>
      </div>
      <div class="flex space-x-2">
        <button
          @click="$emit('view', transaction.id)"
          class="text-primary-600 hover:text-primary-700 text-sm font-medium"
        >
          View Details
        </button>
        <button
          v-if="canPay"
          @click="$emit('pay', transaction.id)"
          class="text-green-600 hover:text-green-700 text-sm font-medium"
        >
          Pay Now
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { format } from 'date-fns'
import { UserIcon } from '@heroicons/vue/24/outline'
import type { Transaction } from '@/stores/transactions'
import { useAuthStore } from '@/stores/auth'

interface Props {
  transaction: Transaction
}

const props = defineProps<Props>()
const authStore = useAuthStore()

defineEmits<{
  view: [id: number]
  pay: [id: number]
}>()

const canPay = computed(() => {
  return props.transaction.internal_status === 'Payment Pending' && 
         (authStore.user?.id === props.transaction.user_id || authStore.isAdmin)
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
</script>
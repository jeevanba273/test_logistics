<template>
  <div class="card hover:shadow-md transition-shadow cursor-pointer" @click="$emit('click')">
    <div class="flex items-center justify-between">
      <div class="flex-1">
        <div class="flex items-center justify-between mb-2">
          <h3 class="text-lg font-semibold text-gray-900">Transaction #{{ transaction.id }}</h3>
          <span
            class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
            :class="getStatusColor(transaction.status)"
          >
            {{ transaction.status }}
          </span>
        </div>
        
        <div class="space-y-1 text-sm text-gray-600">
          <p><span class="font-medium">Amount:</span> ${{ transaction.amount.toFixed(2) }}</p>
          <p><span class="font-medium">Delivery Date:</span> {{ formatDate(transaction.delivery_date) }}</p>
          <p><span class="font-medium">Payment:</span> 
            <span
              class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ml-1"
              :class="getPaymentStatusColor(transaction.payment_status)"
            >
              {{ transaction.payment_status }}
            </span>
          </p>
          <p v-if="transaction.user" class="text-xs text-gray-500">
            User: {{ transaction.user.username }}
          </p>
        </div>
      </div>
      
      <div class="ml-4 flex-shrink-0">
        <ChevronRightIcon class="w-5 h-5 text-gray-400" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ChevronRightIcon } from '@heroicons/vue/24/outline'
import type { Transaction } from '@/stores/transactions'

interface Props {
  transaction: Transaction
}

defineProps<Props>()
defineEmits<{
  click: []
}>()

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
  return new Date(dateString).toLocaleDateString()
}
</script>
<template>
  <div class="max-w-2xl mx-auto py-6 sm:px-6 lg:px-8">
    <div class="px-4 py-6 sm:px-0">
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900">Create Transaction</h1>
        <p class="mt-2 text-gray-600">Create a new shipment transaction</p>
      </div>

      <form @submit.prevent="handleSubmit" class="card space-y-6">
        <div>
          <label for="name" class="block text-sm font-medium text-gray-700">Shipment Name</label>
          <input
            id="name"
            v-model="form.name"
            type="text"
            required
            class="input mt-1"
            placeholder="Enter shipment name"
          />
        </div>

        <div>
          <label for="amount" class="block text-sm font-medium text-gray-700">Amount ($)</label>
          <input
            id="amount"
            v-model.number="form.amount"
            type="number"
            step="0.01"
            min="0"
            required
            class="input mt-1"
            placeholder="Enter amount"
          />
        </div>

        <div>
          <label for="delivery_date" class="block text-sm font-medium text-gray-700">Delivery Date</label>
          <input
            id="delivery_date"
            v-model="form.delivery_date"
            type="date"
            required
            class="input mt-1"
            :min="new Date().toISOString().split('T')[0]"
          />
        </div>

        <div>
          <label for="source_city" class="block text-sm font-medium text-gray-700">Source City</label>
          <input
            id="source_city"
            v-model="form.source_city"
            type="text"
            required
            class="input mt-1"
            placeholder="Enter source city"
          />
        </div>

        <div>
          <label for="destination_city" class="block text-sm font-medium text-gray-700">Destination City</label>
          <input
            id="destination_city"
            v-model="form.destination_city"
            type="text"
            required
            class="input mt-1"
            placeholder="Enter destination city"
          />
        </div>

        <div>
          <label for="status" class="block text-sm font-medium text-gray-700">Status</label>
          <select
            id="status"
            v-model="form.status"
            required
            class="input mt-1"
          >
            <option value="">Select status</option>
            <option value="pending">Pending</option>
            <option value="in_transit">In Transit</option>
            <option value="delivered">Delivered</option>
          </select>
        </div>

        <div>
          <label for="description" class="block text-sm font-medium text-gray-700">Description</label>
          <textarea
            id="description"
            v-model="form.description"
            rows="3"
            class="input mt-1"
            placeholder="Enter description (optional)"
          ></textarea>
        </div>

        <div class="flex items-center justify-end space-x-4">
          <RouterLink to="/transactions" class="btn btn-secondary">
            Cancel
          </RouterLink>
          <button
            type="submit"
            :disabled="transactionsStore.loading"
            class="btn btn-primary"
          >
            <span v-if="transactionsStore.loading">Creating...</span>
            <span v-else>Create Transaction</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { useTransactionsStore } from '@/stores/transactions'

const transactionsStore = useTransactionsStore()
const router = useRouter()

const form = reactive({
  name: '',
  amount: 0,
  delivery_date: '',
  source_city: '',
  destination_city: '',
  status: 'pending',
  description: '',
  type: 'delivery'
})

const handleSubmit = async () => {
  const success = await transactionsStore.createTransaction({
    ...form,
    payment_status: 'pending'
  })
  
  if (success) {
    router.push('/transactions')
  }
}
</script>
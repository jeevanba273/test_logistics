<template>
  <div class="p-6 max-w-2xl mx-auto">
    <div class="animate-fade-in">
      <h1 class="text-3xl font-bold text-gray-900 mb-2">Create Transaction</h1>
      <p class="text-gray-600 mb-8">Start a new shipment request</p>
    </div>

    <form @submit.prevent="handleSubmit" class="space-y-6 animate-slide-up">
      <div class="card">
        <h2 class="text-lg font-semibold text-gray-900 mb-4">Shipment Details</h2>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label for="name" class="block text-sm font-medium text-gray-700 mb-1">
              Shipment Name *
            </label>
            <input
              id="name"
              v-model="form.name"
              type="text"
              required
              class="input-field"
              placeholder="Enter shipment name"
            />
          </div>

          <div>
            <label for="type" class="block text-sm font-medium text-gray-700 mb-1">
              Type *
            </label>
            <select id="type" v-model="form.type" required class="input-field">
              <option value="">Select type</option>
              <option value="edible">Edible</option>
              <option value="fragile">Fragile</option>
              <option value="non-fragile">Non-fragile</option>
            </select>
          </div>

          <div>
            <label for="source_city" class="block text-sm font-medium text-gray-700 mb-1">
              Source City *
            </label>
            <input
              id="source_city"
              v-model="form.source_city"
              type="text"
              required
              class="input-field"
              placeholder="Enter source city"
            />
          </div>

          <div>
            <label for="destination_city" class="block text-sm font-medium text-gray-700 mb-1">
              Destination City *
            </label>
            <input
              id="destination_city"
              v-model="form.destination_city"
              type="text"
              required
              class="input-field"
              placeholder="Enter destination city"
            />
          </div>

          <div class="md:col-span-2">
            <label for="date" class="block text-sm font-medium text-gray-700 mb-1">
              Shipment Date *
            </label>
            <input
              id="date"
              v-model="form.date"
              type="date"
              required
              class="input-field"
            />
          </div>

          <div class="md:col-span-2">
            <label for="description" class="block text-sm font-medium text-gray-700 mb-1">
              Description
            </label>
            <textarea
              id="description"
              v-model="form.description"
              rows="3"
              class="input-field"
              placeholder="Enter additional details about the shipment"
            ></textarea>
          </div>
        </div>
      </div>

      <div class="flex items-center justify-between pt-6">
        <router-link to="/transactions" class="btn-secondary">
          Cancel
        </router-link>
        <button
          type="submit"
          :disabled="isSubmitting"
          class="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <span v-if="isSubmitting" class="flex items-center">
            <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Creating...
          </span>
          <span v-else>Create Transaction</span>
        </button>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useTransactionsStore } from '@/stores/transactions'
import { useToast } from 'vue-toastification'

const router = useRouter()
const transactionsStore = useTransactionsStore()
const toast = useToast()

const isSubmitting = ref(false)

const form = reactive({
  name: '',
  type: '',
  source_city: '',
  destination_city: '',
  date: '',
  description: ''
})

const handleSubmit = async () => {
  isSubmitting.value = true
  try {
    await transactionsStore.createTransaction(form)
    toast.success('Transaction created successfully!')
    router.push('/transactions')
  } catch (error: any) {
    toast.error(error.response?.data?.message || 'Failed to create transaction')
  } finally {
    isSubmitting.value = false
  }
}
</script>
import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/services/api'
import { useAuthStore } from './auth'

export interface Transaction {
  id: number
  name: string
  user_id: number
  type: string
  date: string
  delivery_date: string
  source_city: string
  destination_city: string
  internal_status: string
  delivery_status: string
  description: string
  amount: number
  user: string
}

export const useTransactionsStore = defineStore('transactions', () => {
  const transactions = ref<Transaction[]>([])
  const isLoading = ref(false)
  const authStore = useAuthStore()

  const fetchTransactions = async () => {
    isLoading.value = true
    try {
      const response = await api.get('/api/get', {
        headers: { 'Authentication-Token': authStore.token }
      })
      transactions.value = response.data
    } catch (error) {
      console.error('Failed to fetch transactions:', error)
      transactions.value = []
    } finally {
      isLoading.value = false
    }
  }

  const createTransaction = async (transactionData: Partial<Transaction>) => {
    try {
      const response = await api.post('/api/create', transactionData, {
        headers: { 'Authentication-Token': authStore.token }
      })
      await fetchTransactions() // Refresh the list
      return response.data
    } catch (error) {
      throw error
    }
  }

  const updateTransaction = async (id: number, transactionData: Partial<Transaction>) => {
    try {
      const response = await api.put(`/api/update/${id}`, transactionData, {
        headers: { 'Authentication-Token': authStore.token }
      })
      await fetchTransactions() // Refresh the list
      return response.data
    } catch (error) {
      throw error
    }
  }

  const deleteTransaction = async (id: number) => {
    try {
      const response = await api.delete(`/api/delete/${id}`, {
        headers: { 'Authentication-Token': authStore.token }
      })
      await fetchTransactions() // Refresh the list
      return response.data
    } catch (error) {
      throw error
    }
  }

  const payTransaction = async (id: number) => {
    try {
      const response = await api.get(`/api/pay/${id}`, {
        headers: { 'Authentication-Token': authStore.token }
      })
      await fetchTransactions() // Refresh the list
      return response.data
    } catch (error) {
      throw error
    }
  }

  const updateDeliveryStatus = async (id: number, deliveryStatus: string) => {
    try {
      const response = await api.put(`/api/update_delivery_status/${id}`, 
        { delivery_status: deliveryStatus }, 
        {
          headers: { 'Authentication-Token': authStore.token }
        }
      )
      await fetchTransactions() // Refresh the list
      return response.data
    } catch (error) {
      throw error
    }
  }

  const updateAmount = async (id: number, amount: number) => {
    try {
      const response = await api.post(`/api/update_amount/${id}`, 
        { amount }, 
        {
          headers: { 'Authentication-Token': authStore.token }
        }
      )
      await fetchTransactions() // Refresh the list
      return response.data
    } catch (error) {
      throw error
    }
  }

  const updateDeliveryDate = async (id: number, deliveryDate: string) => {
    try {
      const response = await api.post(`/api/update_delivery_date/${id}`, 
        { delivery_date: deliveryDate }, 
        {
          headers: { 'Authentication-Token': authStore.token }
        }
      )
      await fetchTransactions() // Refresh the list
      return response.data
    } catch (error) {
      throw error
    }
  }

  const getTransactionById = async (id: number) => {
    try {
      const response = await api.get(`/api/review_transaction/${id}`, {
        headers: { 'Authentication-Token': authStore.token }
      })
      return response.data
    } catch (error) {
      throw error
    }
  }

  return {
    transactions,
    isLoading,
    fetchTransactions,
    createTransaction,
    updateTransaction,
    deleteTransaction,
    payTransaction,
    updateDeliveryStatus,
    updateAmount,
    updateDeliveryDate,
    getTransactionById
  }
})
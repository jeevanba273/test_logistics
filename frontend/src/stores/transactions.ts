import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/services/api'
import { useToast } from 'vue-toastification'

const toast = useToast()

export interface Transaction {
  id: number
  user_id: number
  amount: number
  delivery_date: string
  status: string
  payment_status: string
  created_at: string
  updated_at: string
  name?: string
  type?: string
  date?: string
  source_city?: string
  destination_city?: string
  description?: string
  user?: {
    username: string
    email: string
  }
}

export const useTransactionsStore = defineStore('transactions', () => {
  const transactions = ref<Transaction[]>([])
  const loading = ref(false)

  const fetchTransactions = async () => {
    loading.value = true
    try {
      console.log('Fetching transactions...')
      const response = await api.get('/api/get')
      console.log('Transactions response:', response.data)
      transactions.value = response.data
    } catch (error: any) {
      console.error('Failed to fetch transactions:', error)
      toast.error('Failed to fetch transactions')
    } finally {
      loading.value = false
    }
  }

  const createTransaction = async (transactionData: Partial<Transaction>) => {
    loading.value = true
    try {
      console.log('Creating transaction:', transactionData)
      const response = await api.post('/api/create', transactionData)
      console.log('Create transaction response:', response.data)
      await fetchTransactions()
      toast.success('Transaction created successfully!')
      return true
    } catch (error: any) {
      console.error('Failed to create transaction:', error)
      const errorMessage = error.response?.data?.error || error.response?.data?.message || 'Failed to create transaction'
      toast.error(errorMessage)
      return false
    } finally {
      loading.value = false
    }
  }

  const updateTransaction = async (id: number, transactionData: Partial<Transaction>) => {
    loading.value = true
    try {
      await api.put(`/api/update/${id}`, transactionData)
      await fetchTransactions()
      toast.success('Transaction updated successfully!')
      return true
    } catch (error: any) {
      const errorMessage = error.response?.data?.error || error.response?.data?.message || 'Failed to update transaction'
      toast.error(errorMessage)
      return false
    } finally {
      loading.value = false
    }
  }

  const deleteTransaction = async (id: number) => {
    loading.value = true
    try {
      await api.delete(`/api/delete/${id}`)
      await fetchTransactions()
      toast.success('Transaction deleted successfully!')
      return true
    } catch (error: any) {
      const errorMessage = error.response?.data?.error || error.response?.data?.message || 'Failed to delete transaction'
      toast.error(errorMessage)
      return false
    } finally {
      loading.value = false
    }
  }

  const payTransaction = async (id: number) => {
    loading.value = true
    try {
      await api.get(`/api/pay/${id}`)
      await fetchTransactions()
      toast.success('Payment processed successfully!')
      return true
    } catch (error: any) {
      const errorMessage = error.response?.data?.error || error.response?.data?.message || 'Payment failed'
      toast.error(errorMessage)
      return false
    } finally {
      loading.value = false
    }
  }

  const updateAmount = async (id: number, amount: number) => {
    loading.value = true
    try {
      await api.post(`/api/update_amount/${id}`, { amount })
      await fetchTransactions()
      toast.success('Amount updated successfully!')
      return true
    } catch (error: any) {
      const errorMessage = error.response?.data?.error || error.response?.data?.message || 'Failed to update amount'
      toast.error(errorMessage)
      return false
    } finally {
      loading.value = false
    }
  }

  const updateDeliveryStatus = async (id: number, delivery_status: string) => {
    loading.value = true
    try {
      await api.put(`/api/update_delivery_status/${id}`, { delivery_status })
      await fetchTransactions()
      toast.success('Delivery status updated successfully!')
      return true
    } catch (error: any) {
      const errorMessage = error.response?.data?.error || error.response?.data?.message || 'Failed to update delivery status'
      toast.error(errorMessage)
      return false
    } finally {
      loading.value = false
    }
  }

  const updateDeliveryDate = async (id: number, delivery_date: string) => {
    loading.value = true
    try {
      await api.put(`/api/update_delivery_date/${id}`, { delivery_date })
      await fetchTransactions()
      toast.success('Delivery date updated successfully!')
      return true
    } catch (error: any) {
      const errorMessage = error.response?.data?.error || error.response?.data?.message || 'Failed to update delivery date'
      toast.error(errorMessage)
      return false
    } finally {
      loading.value = false
    }
  }

  return {
    transactions,
    loading,
    fetchTransactions,
    createTransaction,
    updateTransaction,
    deleteTransaction,
    payTransaction,
    updateAmount,
    updateDeliveryStatus,
    updateDeliveryDate
  }
})
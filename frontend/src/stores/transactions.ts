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
      const response = await api.get('/get')
      transactions.value = response.data
    } catch (error: any) {
      toast.error('Failed to fetch transactions')
    } finally {
      loading.value = false
    }
  }

  const createTransaction = async (transactionData: Partial<Transaction>) => {
    loading.value = true
    try {
      await api.post('/create', transactionData)
      await fetchTransactions()
      toast.success('Transaction created successfully!')
      return true
    } catch (error: any) {
      toast.error(error.response?.data?.message || 'Failed to create transaction')
      return false
    } finally {
      loading.value = false
    }
  }

  const updateTransaction = async (id: number, transactionData: Partial<Transaction>) => {
    loading.value = true
    try {
      await api.put(`/update/${id}`, transactionData)
      await fetchTransactions()
      toast.success('Transaction updated successfully!')
      return true
    } catch (error: any) {
      toast.error(error.response?.data?.message || 'Failed to update transaction')
      return false
    } finally {
      loading.value = false
    }
  }

  const deleteTransaction = async (id: number) => {
    loading.value = true
    try {
      await api.delete(`/delete/${id}`)
      await fetchTransactions()
      toast.success('Transaction deleted successfully!')
      return true
    } catch (error: any) {
      toast.error(error.response?.data?.message || 'Failed to delete transaction')
      return false
    } finally {
      loading.value = false
    }
  }

  const payTransaction = async (id: number) => {
    loading.value = true
    try {
      await api.get(`/pay/${id}`)
      await fetchTransactions()
      toast.success('Payment processed successfully!')
      return true
    } catch (error: any) {
      toast.error(error.response?.data?.message || 'Payment failed')
      return false
    } finally {
      loading.value = false
    }
  }

  const updateAmount = async (id: number, amount: number) => {
    loading.value = true
    try {
      await api.post(`/update_amount/${id}`, { amount })
      await fetchTransactions()
      toast.success('Amount updated successfully!')
      return true
    } catch (error: any) {
      toast.error(error.response?.data?.message || 'Failed to update amount')
      return false
    } finally {
      loading.value = false
    }
  }

  const updateDeliveryStatus = async (id: number, status: string) => {
    loading.value = true
    try {
      await api.put(`/update_delivery_status/${id}`, { status })
      await fetchTransactions()
      toast.success('Delivery status updated successfully!')
      return true
    } catch (error: any) {
      toast.error(error.response?.data?.message || 'Failed to update delivery status')
      return false
    } finally {
      loading.value = false
    }
  }

  const updateDeliveryDate = async (id: number, delivery_date: string) => {
    loading.value = true
    try {
      await api.post(`/update_delivery_date/${id}`, { delivery_date })
      await fetchTransactions()
      toast.success('Delivery date updated successfully!')
      return true
    } catch (error: any) {
      toast.error(error.response?.data?.message || 'Failed to update delivery date')
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
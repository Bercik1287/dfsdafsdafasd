import { ref } from 'vue'

export const useTrasy = () => {
  const loading = ref(false)
  const error = ref(null)
  const success = ref(false)

  const createTrasa = async (trasaData) => {
    try {
      loading.value = true
      error.value = null
      success.value = false

      const response = await $fetch('http://localhost:8000/transport/trasyv2', {
        method: 'POST',
        body: JSON.stringify(trasaData),
        headers: {
          'Content-Type': 'application/json'
        }
      })

      success.value = true
      return response
    } catch (err) {
      if (err.data?.detail) {
        error.value = err.data.detail
      } else {
        error.value = 'Wystąpił błąd podczas tworzenia trasy'
        console.error('Szczegóły błędu:', err)
      }
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    loading,
    error,
    success,
    createTrasa
  }
}
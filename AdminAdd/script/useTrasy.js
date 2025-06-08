import { ref, computed, onMounted } from 'vue'

export const useTrasy = () => {
  const trasy = ref([])
  const loading = ref(true)
  const error = ref(null)

  const fetchTrasy = async () => {
    try {
      const { data } = await useFetch('http://localhost:8000/transport/trasy')
      trasy.value = data.value || []
    } catch (err) {
      error.value = 'Błąd pobierania tras'
      console.error(err)
    } finally {
      loading.value = false
    }
  }

  const sortedTrasy = computed(() => {
    return [...trasy.value].sort((a, b) => a.nazwa.localeCompare(b.nazwa))
  })

  return {
    trasy,
    sortedTrasy,
    loading,
    error,
    fetchTrasy
  }
}
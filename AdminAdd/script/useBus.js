import { ref, computed } from 'vue'

export const useBus = () => {
  const buses = ref([])
  const loading = ref(true)
  const error = ref(null)

  const fetchBus = async () => {
    try {
      loading.value = true
      const { data } = await useFetch('http://localhost:8000/transport/autobusy')
      buses.value = data.value || []
    } catch (err) {
      error.value = 'Błąd pobierania autobusów'
      console.error('Błąd pobierania autobusów:', err)
    } finally {
      loading.value = false
    }
  }

  const sortedBuses = computed(() => {
    return [...buses.value].sort((a, b) => 
      `${a.marka} ${a.model}`.localeCompare(`${b.marka} ${b.model}`)
    )
  })

  return {
    buses,
    sortedBuses,
    loading,
    error,
    fetchBus
  }
}
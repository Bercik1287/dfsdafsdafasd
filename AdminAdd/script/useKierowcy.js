import { ref, computed } from 'vue'

export const useKierowcy = () => {
  const kierowcy = ref([])
  const loading = ref(false)
  const error = ref(null)

  const fetchKierowcy = async () => {
    try {
      loading.value = true
      const { data } = await useFetch('http://localhost:8000/transport/kierowcy')
      kierowcy.value = data.value || []
    } catch (err) {
      error.value = 'Błąd pobierania kierowców'
      console.error('Błąd:', err)
    } finally {
      loading.value = false
    }
  }

  const sortedKierowcy = computed(() => {
    return [...kierowcy.value].sort((a, b) => 
      a.nazwisko.localeCompare(b.nazwisko)
    )
  })

  return {
    kierowcy,
    sortedKierowcy,
    loading,
    error,
    fetchKierowcy
  }
}
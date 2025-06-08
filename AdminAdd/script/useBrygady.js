import { ref, computed, onMounted } from 'vue'

export const useBrygady = () => {
  const brygady = ref([])
  const loading = ref(true)
  const error = ref(null)

  const fetchBrygady = async () => {
    try {
      const { data } = await useFetch('http://localhost:8000/transport/brygady')
      brygady.value = data.value || []
    } catch (err) {
      error.value = 'Błąd pobierania brygad'
      console.error(err)
    } finally {
      loading.value = false
    }
  }

  const sortedBrygady = computed(() => {
    return [...brygady.value].sort((a, b) => a.nazwa.localeCompare(b.nazwa))
  })

  return {
    brygady,
    sortedBrygady,
    loading,
    error,
    fetchBrygady
  }
}
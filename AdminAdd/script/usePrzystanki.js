import { ref, computed } from 'vue' // lub z 'nuxt/app' jeśli Nuxt 3

//przystanki 
export const usePrzystanki = () => {
  const przystanki = ref([])
  const loading = ref(true)
  const error = ref(null)

  const fetchPrzystanki = async () => {
    try {
      const { data } = await useFetch('http://localhost:8000/transport/przystanki')
      przystanki.value = data.value || []
    } catch (err) {
      error.value = 'Błąd pobierania przystanków'
      console.error(err)
    } finally {
      loading.value = false
    }
  }

  const sortedPrzystanki = computed(() => {
    return [...przystanki.value].sort((a, b) => 
      a.nazwa.localeCompare(b.nazwa)
    )
  })

  return {
    przystanki,
    sortedPrzystanki,
    loading,
    error,
    fetchPrzystanki
  }
}
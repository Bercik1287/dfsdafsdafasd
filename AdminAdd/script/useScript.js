import { ref, computed } from 'vue' // lub z 'nuxt/app' jeśli Nuxt 3

export const useLines = () => {
  const loading = ref(true)
  const error = ref(null)
  const lines = ref([])
  const selectedLineId = ref(null)

  const fetchLines = async () => {
    try {
      const res = await fetch('http://localhost:8000/transport/linie')
      lines.value = await res.json()
    } catch (err) {
      error.value = 'Błąd pobierania listy linii'
      console.error(err)
    } finally {
      loading.value = false
    }
  }

  const sortedLines = computed(() => {
    return [...lines.value].sort((a, b) => a.numer - b.numer)
  })

  return {
    loading,
    error,
    lines,
    selectedLineId,
    sortedLines,
    fetchLines
  }
}


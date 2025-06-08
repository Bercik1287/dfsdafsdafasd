<template>
  <div class="edit-route-container">
    <h1 class="text-xl font-bold mb-4">Edytuj trasy</h1>
    
    <!-- Lista tras -->
    <div v-if="!selectedRoute" class="route-list-container">
      <div v-if="loading" class="loading">
        Ładowanie tras...
      </div>
      
      <div v-else-if="error" class="error">
        {{ error }}
      </div>
      
      <div v-else class="route-list">
        <div class="search-container">
          <input
            v-model="searchTerm"
            type="text"
            placeholder="Szukaj po nazwie trasy..."
            class="search-input"
          />
        </div>
        
        <div class="route-grid">
          <div
            v-for="route in filteredRoutes"
            :key="route.id"
            @click="selectRoute(route)"
            class="route-card"
          >
            <div class="route-info">
              <h3>{{ route.nazwa || `Trasa ${route.id}` }}</h3>
              <p class="text-sm text-gray-300">ID: {{ route.id }}</p>
            </div>
            <button class="edit-btn">
              Edytuj
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Formularz edycji -->
    <div v-if="selectedRoute" class="edit-form-container">
      <button @click="goBack" class="back-btn">
        ← Powrót do listy
      </button>
      
      <form @submit.prevent="updateRoute" class="edit-form">
        <h2>Edytuj trasę: {{ originalRoute.nazwa || `Trasa ${originalRoute.id}` }}</h2>
        
        <!-- Nazwa trasy -->
        <div class="form-group">
          <label for="nazwa">Nazwa trasy:</label>
          <input
            id="nazwa"
            v-model="selectedRoute.nazwa"
            type="text"
            placeholder="Wprowadź nazwę trasy (opcjonalnie)"
          />
        </div>

        <!-- Warianty trasy -->
        <div class="form-section">
          <h3 class="section-title">Warianty trasy</h3>
          <div v-if="routeVariants.length === 0" class="no-variants">
            Brak wariantów dla tej trasy
          </div>
          <div v-else class="variants-list">
            <div
              v-for="variant in routeVariants"
              :key="variant.id"
              class="variant-card"
            >
              <div class="variant-header">
                <h4>{{ variant.nazwa }}</h4>
                <span class="variant-code">{{ variant.kod_wariantu }}</span>
              </div>
              
              <!-- Godziny odjazdu dla wariantu -->
              <div class="departure-times">
                <label class="variant-label">Godziny odjazdu:</label>
                <div class="times-grid">
                  <div
                    v-for="(time, timeIndex) in variant.godziny_odjazdu"
                    :key="timeIndex"
                    class="time-item"
                  >
                    <input
                      v-model="variant.godziny_odjazdu[timeIndex]"
                      type="time"
                      class="time-input"
                    />
                    <button
                      @click="removeTime(variant, timeIndex)"
                      type="button"
                      class="remove-time-btn"
                      v-if="variant.godziny_odjazdu.length > 1"
                    >
                      ×
                    </button>
                  </div>
                </div>
                <button
                  @click="addTime(variant)"
                  type="button"
                  class="add-time-btn"
                >
                  + Dodaj godzinę
                </button>
              </div>

              <!-- Przystanki wariantu -->
              <div class="variant-stops">
                <label class="variant-label">Przystanki:</label>
                <div v-if="variant.przystanki && variant.przystanki.length > 0" class="stops-list">
                  <div
                    v-for="(stop, stopIndex) in variant.przystanki"
                    :key="stopIndex"
                    class="stop-item"
                  >
                    <span class="stop-order">{{ stopIndex + 1 }}.</span>
                    <span class="stop-name">{{ stop.nazwa }}</span>
                    <span class="stop-address">({{ stop.ulica }})</span>
                  </div>
                </div>
                <div v-else class="no-stops">
                  Brak przypisanych przystanków
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Komunikaty -->
        <div v-if="updateError" class="error mt-2">
          {{ updateError }}
        </div>
        <div v-if="updateSuccess" class="success mt-2">
          Trasa została pomyślnie zaktualizowana!
        </div>

        <!-- Przyciski akcji -->
        <div class="form-actions">
          <button
            type="submit"
            :disabled="updateLoading || !hasChanges"
            class="save-btn"
          >
            {{ updateLoading ? 'Zapisywanie...' : 'Zapisz zmiany' }}
          </button>
          
          <button
            type="button"
            @click="resetForm"
            class="reset-btn"
          >
            Resetuj
          </button>
          
          <button
            type="button"
            @click="deleteRoute"
            :disabled="deleteLoading"
            class="delete-btn"
          >
            {{ deleteLoading ? 'Usuwanie...' : 'Usuń trasę' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

// Reactive data
const routes = ref([])
const routeVariants = ref([])
const loading = ref(true)
const variantsLoading = ref(false)
const error = ref('')
const selectedRoute = ref(null)
const originalRoute = ref(null)
const searchTerm = ref('')
const updateLoading = ref(false)
const deleteLoading = ref(false)
const updateError = ref('')
const updateSuccess = ref(false)

// Computed properties
const filteredRoutes = computed(() => {
  if (!searchTerm.value) return routes.value
  
  const term = searchTerm.value.toLowerCase()
  return routes.value.filter(route => 
    (route.nazwa && route.nazwa.toLowerCase().includes(term)) ||
    route.id.toString().includes(term)
  )
})

const hasChanges = computed(() => {
  if (!selectedRoute.value || !originalRoute.value) return false
  
  // Check if route name changed
  if (selectedRoute.value.nazwa !== originalRoute.value.nazwa) return true
  
  // Check if any variant times changed
  return routeVariants.value.some(variant => {
    const originalVariant = originalRoute.value.variants?.find(v => v.id === variant.id)
    if (!originalVariant) return true
    
    return JSON.stringify(variant.godziny_odjazdu) !== JSON.stringify(originalVariant.godziny_odjazdu)
  })
})

// Methods
const fetchRoutes = async () => {
  try {
    loading.value = true
    error.value = ''
    
    const response = await $fetch('http://localhost:8000/transport/trasy')
    routes.value = response || []
  } catch (err) {
    error.value = 'Błąd podczas pobierania tras'
    console.error('Błąd pobierania tras:', err)
  } finally {
    loading.value = false
  }
}

const fetchRouteVariants = async (routeId) => {
  try {
    variantsLoading.value = true
    
    // Fetch variants for route
    const variantsResponse = await $fetch('http://localhost:8000/transport/warianty')
    
    // Filter variants that belong to this route (you may need to adjust this based on your API structure)
    // For now, we'll fetch all variants and you may need to implement a specific endpoint
    const allVariants = variantsResponse || []
    
    // Since we don't have a direct route-variant relationship endpoint,
    // we'll need to implement this based on your database structure
    // This is a placeholder - adjust based on your actual API
    routeVariants.value = allVariants.filter(variant => {
      // You'll need to implement the logic to filter variants by route
      // This might require a new API endpoint or modification of existing ones
      return true // placeholder
    })

    // For each variant, try to fetch its stops
    for (let variant of routeVariants.value) {
      try {
        // Parse godziny_odjazdu if it's a string
        if (typeof variant.godziny_odjazdu === 'string') {
          variant.godziny_odjazdu = JSON.parse(variant.godziny_odjazdu)
        }
        if (!Array.isArray(variant.godziny_odjazdu)) {
          variant.godziny_odjazdu = []
        }
        
        // Fetch stops for this variant (you may need to implement this endpoint)
        // variant.przystanki = await fetchVariantStops(variant.id)
        variant.przystanki = [] // placeholder
      } catch (err) {
        console.error(`Error processing variant ${variant.id}:`, err)
        variant.godziny_odjazdu = []
        variant.przystanki = []
      }
    }
    
  } catch (err) {
    console.error('Błąd pobierania wariantów:', err)
    routeVariants.value = []
  } finally {
    variantsLoading.value = false
  }
}

const selectRoute = async (route) => {
  selectedRoute.value = { ...route }
  originalRoute.value = { ...route }
  updateError.value = ''
  updateSuccess.value = false
  
  await fetchRouteVariants(route.id)
  
  // Store original variants for comparison
  originalRoute.value.variants = JSON.parse(JSON.stringify(routeVariants.value))
}

const goBack = () => {
  selectedRoute.value = null
  originalRoute.value = null
  routeVariants.value = []
  updateError.value = ''
  updateSuccess.value = false
}

const resetForm = () => {
  if (originalRoute.value) {
    selectedRoute.value = { ...originalRoute.value }
    routeVariants.value = JSON.parse(JSON.stringify(originalRoute.value.variants || []))
    updateError.value = ''
    updateSuccess.value = false
  }
}

const addTime = (variant) => {
  if (!variant.godziny_odjazdu) {
    variant.godziny_odjazdu = []
  }
  variant.godziny_odjazdu.push('')
}

const removeTime = (variant, index) => {
  variant.godziny_odjazdu.splice(index, 1)
}

const updateRoute = async () => {
  try {
    updateLoading.value = true
    updateError.value = ''
    updateSuccess.value = false

    // Update route basic info
    if (selectedRoute.value.nazwa !== originalRoute.value.nazwa) {
      const routeUpdateData = {
        id: selectedRoute.value.id,
        nazwa: selectedRoute.value.nazwa
      }

      await $fetch('http://localhost:8000/transport/trasy', {
        method: 'PUT',
        body: JSON.stringify(routeUpdateData),
        headers: {
          'Content-Type': 'application/json'
        }
      })
    }

    // Update each variant's departure times
    for (const variant of routeVariants.value) {
      const originalVariant = originalRoute.value.variants?.find(v => v.id === variant.id)
      
      if (!originalVariant || 
          JSON.stringify(variant.godziny_odjazdu) !== JSON.stringify(originalVariant.godziny_odjazdu)) {
        
        const variantUpdateData = {
          id: variant.id,
          nazwa: variant.nazwa,
          kod_wariantu: variant.kod_wariantu,
          godziny_odjazdu: variant.godziny_odjazdu.filter(time => time !== '')
        }

        await $fetch('http://localhost:8000/transport/warianty', {
          method: 'PUT',
          body: JSON.stringify(variantUpdateData),
          headers: {
            'Content-Type': 'application/json'
          }
        })
      }
    }

    updateSuccess.value = true
    originalRoute.value = { ...selectedRoute.value, variants: JSON.parse(JSON.stringify(routeVariants.value)) }
    
    // Update the route in the list
    const routeIndex = routes.value.findIndex(r => r.id === selectedRoute.value.id)
    if (routeIndex !== -1) {
      routes.value[routeIndex] = { ...selectedRoute.value }
    }

    // Auto hide success message after 3 seconds
    setTimeout(() => {
      updateSuccess.value = false
    }, 3000)

  } catch (err) {
    if (err.data?.detail) {
      updateError.value = err.data.detail
    } else {
      updateError.value = 'Wystąpił błąd podczas aktualizacji trasy'
    }
    console.error('Błąd aktualizacji trasy:', err)
  } finally {
    updateLoading.value = false
  }
}

const deleteRoute = async () => {
  if (!confirm(`Czy na pewno chcesz usunąć trasę "${selectedRoute.value.nazwa || selectedRoute.value.id}"?`)) {
    return
  }

  try {
    deleteLoading.value = true
    updateError.value = ''

    await $fetch(`http://localhost:8000/transport/trasy/${selectedRoute.value.id}`, {
      method: 'DELETE'
    })

    // Remove from local list
    routes.value = routes.value.filter(r => r.id !== selectedRoute.value.id)
    
    // Go back to list
    goBack()

  } catch (err) {
    updateError.value = 'Wystąpił błąd podczas usuwania trasy'
    console.error('Błąd usuwania trasy:', err)
  } finally {
    deleteLoading.value = false
  }
}

// Lifecycle
onMounted(() => {
  fetchRoutes()
})
</script>

<style scoped>
.edit-route-container {
  background-color: var(--moj_srodek);
  border-radius: 15px;
  padding: 20px;
  max-width: 1200px;
}

h1, h2 {
  color: white;
  text-align: center;
  margin-bottom: 20px;
}

.loading, .error {
  text-align: center;
  padding: 20px;
  color: white;
  font-size: 18px;
}

.error {
  color: #ff6b6b;
}

.success {
  color: #51cf66;
  text-align: center;
  padding: 10px;
  background-color: rgba(81, 207, 102, 0.1);
  border-radius: 5px;
  margin-top: 10px;
}

.search-container {
  margin-bottom: 20px;
}

.search-input {
  width: 100%;
  padding: 12px;
  border-radius: 8px;
  border: 1px solid #ccc;
  font-size: 16px;
  background-color: white;
}

.route-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 15px;
}

.route-card {
  background-color: var(--moj_szary);
  border-radius: 10px;
  padding: 15px;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.route-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.route-info h3 {
  color: white;
  font-size: 18px;
  font-weight: bold;
  margin: 0 0 5px 0;
}

.route-info p {
  color: #ccc;
  margin: 0;
}

.edit-btn {
  background-color: var(--moj_zielony);
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s;
}

.edit-btn:hover {
  background-color: #45a049;
}

.back-btn {
  background-color: #6c757d;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  margin-bottom: 20px;
  font-size: 16px;
  transition: background-color 0.3s;
}

.back-btn:hover {
  background-color: #5a6268;
}

.edit-form {
  background-color: var(--moj_szary);
  padding: 20px;
  border-radius: 15px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  color: white;
  font-size: 18px;
  margin-bottom: 8px;
  font-weight: bold;
}

.form-group input {
  width: 100%;
  padding: 12px;
  border-radius: 8px;
  border: 1px solid #ccc;
  font-size: 16px;
  background-color: #f9f9f9;
}

.form-section {
  margin: 30px 0;
  padding: 20px;
  background-color: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
}

.section-title {
  color: white;
  font-size: 20px;
  margin-bottom: 15px;
  font-weight: bold;
}

.no-variants, .no-stops {
  color: #ccc;
  text-align: center;
  padding: 20px;
  font-style: italic;
}

.variants-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.variant-card {
  background-color: rgba(255, 255, 255, 0.1);
  padding: 20px;
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.variant-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.variant-header h4 {
  color: white;
  font-size: 18px;
  margin: 0;
}

.variant-code {
  background-color: var(--moj_zielony);
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: bold;
}

.variant-label {
  color: white;
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 10px;
  display: block;
}

.departure-times {
  margin-bottom: 20px;
}

.times-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 10px;
  margin-bottom: 10px;
}

.time-item {
  display: flex;
  align-items: center;
  gap: 5px;
}

.time-input {
  flex: 1;
  padding: 8px;
  border-radius: 5px;
  border: 1px solid #ccc;
  font-size: 14px;
}

.remove-time-btn {
  background-color: #dc3545;
  color: white;
  border: none;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.add-time-btn {
  background-color: var(--moj_zielony);
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
}

.variant-stops {
  margin-top: 20px;
}

.stops-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.stop-item {
  display: flex;
  align-items: center;
  gap: 10px;
  color: white;
  padding: 8px;
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 5px;
}

.stop-order {
  font-weight: bold;
  color: var(--moj_zielony);
  min-width: 30px;
}

.stop-name {
  font-weight: bold;
}

.stop-address {
  color: #ccc;
  font-size: 14px;
}

.form-actions {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  justify-content: center;
  margin-top: 20px;
}

.save-btn,
.reset-btn,
.delete-btn {
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s;
  min-width: 120px;
}

.save-btn {
  background-color: var(--moj_zielony);
  color: white;
}

.save-btn:hover:not(:disabled) {
  background-color: #45a049;
}

.save-btn:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.reset-btn {
  background-color: #ffc107;
  color: #212529;
}

.reset-btn:hover {
  background-color: #e0a800;
}

.delete-btn {
  background-color: #dc3545;
  color: white;
}

.delete-btn:hover:not(:disabled) {
  background-color: #c82333;
}

.delete-btn:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .route-grid {
    grid-template-columns: 1fr;
  }
  
  .times-grid {
    grid-template-columns: 1fr;
  }
  
  .form-actions {
    flex-direction: column;
  }
  
  .save-btn,
  .reset-btn,
  .delete-btn {
    width: 100%;
  }
  
  .variant-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
}
</style>
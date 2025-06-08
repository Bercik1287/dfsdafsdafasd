<template>
  <div class="container">
    <h1>Edytuj Linie</h1>
    
    <!-- Line Selection -->
    <div class="selection-section">
      <label for="lineSelect" class="block font-semibold">Wybierz linię do edycji:</label>
      <select 
        id="lineSelect" 
        v-model="selectedLineId" 
        @change="loadLineData"
        class="w-full border rounded px-3 py-2"
      >
        <option value="" disabled>Wybierz linię</option>
        <option 
          v-for="line in sortedLines" 
          :key="line.id" 
          :value="line.id"
        >
          Linia {{ line.numer }} - {{ line.kierunek }}
        </option>
      </select>
    </div>

    <!-- Edit Form -->
    <form v-if="selectedLine" @submit.prevent="updateLine" class="edit-form">
      <div>
        <label for="number" class="block font-semibold">Numer:</label>
        <input
          id="number"
          v-model="selectedLine.numer"
          type="text"
          class="w-full border rounded px-3 py-2"
          required
        />
      </div>
      
      <div>
        <label for="kierunek" class="block font-semibold">Kierunek:</label>
        <input
          id="kierunek"
          v-model="selectedLine.kierunek"
          type="text"
          class="w-full border rounded px-3 py-2"
          required
        />
      </div>
      
      <div>
        <label for="opis" class="block font-semibold">Opis:</label>
        <input
          id="opis"
          v-model="selectedLine.opis"
          type="text"
          class="w-full border rounded px-3 py-2"
          required
        />
      </div>

      <!-- Routes Assignment Section -->
      <div class="routes-section">
        <h3>Przypisane trasy:</h3>
        <div v-if="assignedRoutes.length > 0" class="assigned-routes">
          <div 
            v-for="route in assignedRoutes" 
            :key="route.id"
            class="route-item"
          >
            <span>{{ route.nazwa }}</span>
            <button 
              @click="removeRouteFromLine(route.id)"
              type="button"
              class="remove-btn"
            >
              Usuń
            </button>
          </div>
        </div>
        <p v-else class="no-routes">Brak przypisanych tras</p>

        <!-- Add Route Section -->
        <div class="add-route-section">
          <select 
            v-model="selectedRouteToAdd"
            class="route-select"
          >
            <option value="" disabled>Wybierz trasę do dodania</option>
            <option 
              v-for="route in availableRoutes" 
              :key="route.id" 
              :value="route.id"
            >
              {{ route.nazwa }}
            </option>
          </select>
          <button 
            @click="addRouteToLine"
            type="button"
            class="add-route-btn"
            :disabled="!selectedRouteToAdd"
          >
            Dodaj trasę
          </button>
        </div>
      </div>

      <div class="form-actions">
        <button
          type="submit"
          :disabled="loading"
          class="save-btn"
        >
          {{ loading ? 'Zapisywanie...' : 'Zapisz zmiany' }}
        </button>
        
        <button
          @click="cancelEdit"
          type="button"
          class="cancel-btn"
        >
          Anuluj
        </button>
      </div>

      <div v-if="error" class="text-red-500 mt-2">
        {{ error }}
      </div>
      <div v-if="success" class="text-green-500 mt-2">
        Linia została pomyślnie zaktualizowana!
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'

const lines = ref([])
const routes = ref([])
const selectedLineId = ref('')
const selectedLine = ref(null)
const assignedRoutes = ref([])
const selectedRouteToAdd = ref('')
const loading = ref(false)
const error = ref('')
const success = ref(false)

const sortedLines = computed(() => {
  return [...lines.value].sort((a, b) => a.numer - b.numer)
})

const availableRoutes = computed(() => {
  const assignedIds = assignedRoutes.value.map(r => r.id)
  return routes.value.filter(route => !assignedIds.includes(route.id))
})

const fetchLines = async () => {
  try {
    const response = await $fetch('http://localhost:8000/transport/linie')
    lines.value = response
  } catch (err) {
    error.value = 'Błąd pobierania linii'
    console.error(err)
  }
}

const fetchRoutes = async () => {
  try {
    const response = await $fetch('http://localhost:8000/transport/trasy')
    routes.value = response
  } catch (err) {
    error.value = 'Błąd pobierania tras'
    console.error(err)
  }
}

const loadLineData = async () => {
  if (!selectedLineId.value) return
  
  try {
    // Load line details
    const lineResponse = await $fetch(`http://localhost:8000/transport/linie/${selectedLineId.value}`)
    selectedLine.value = { ...lineResponse }
    
    // Load assigned routes
    const routesResponse = await $fetch(`http://localhost:8000/transport/linie/${selectedLineId.value}/trasy`)
    assignedRoutes.value = routesResponse
    
    error.value = ''
  } catch (err) {
    error.value = 'Błąd ładowania danych linii'
    console.error(err)
  }
}

const updateLine = async () => {
  try {
    loading.value = true
    error.value = ''
    success.value = false

    const updateData = {
      id: selectedLine.value.id,
      numer: selectedLine.value.numer,
      kierunek: selectedLine.value.kierunek,
      opis: selectedLine.value.opis
    }

    await $fetch('http://localhost:8000/transport/linie', {
      method: 'PUT',
      body: updateData,
      headers: {
        'Content-Type': 'application/json'
      }
    })

    success.value = true
    
    // Refresh lines list
    await fetchLines()
    
  } catch (err) {
    if (err.data?.detail) {
      error.value = err.data.detail
    } else {
      error.value = 'Wystąpił błąd podczas aktualizacji linii'
    }
    console.error(err)
  } finally {
    loading.value = false
  }
}

const addRouteToLine = async () => {
  if (!selectedRouteToAdd.value || !selectedLineId.value) return
  
  try {
    await $fetch(`http://localhost:8000/transport/linie/${selectedLineId.value}/trasy/${selectedRouteToAdd.value}`, {
      method: 'POST'
    })
    
    // Refresh assigned routes
    await loadLineData()
    selectedRouteToAdd.value = ''
    
  } catch (err) {
    error.value = 'Błąd dodawania trasy do linii'
    console.error(err)
  }
}

const removeRouteFromLine = async (routeId) => {
  try {
    await $fetch(`http://localhost:8000/transport/linie/${selectedLineId.value}/trasy/${routeId}`, {
      method: 'DELETE'
    })
    
    // Refresh assigned routes
    await loadLineData()
    
  } catch (err) {
    error.value = 'Błąd usuwania trasy z linii'
    console.error(err)
  }
}

const cancelEdit = () => {
  selectedLineId.value = ''
  selectedLine.value = null
  assignedRoutes.value = []
  selectedRouteToAdd.value = ''
  error.value = ''
  success.value = false
}

onMounted(async () => {
  await fetchLines()
  await fetchRoutes()
})
</script>

<style scoped>
.container {
  background-color: var(--moj_srodek);
  border-radius: 15px;
  padding: 20px;
  margin: 20px auto;
  max-width: 800px;
}

.selection-section {
  margin-bottom: 30px;
}

.edit-form {
  background-color: var(--moj_szary);
  padding: 20px;
  border-radius: 15px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}

.routes-section {
  margin-top: 30px;
  border-top: 1px solid #ccc;
  padding-top: 20px;
}

.assigned-routes {
  margin: 15px 0;
}

.route-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  background-color: var(--moj_srodek);
  border-radius: 8px;
  margin-bottom: 10px;
}

.route-item span {
  color: white;
  font-weight: 500;
}

.remove-btn {
  background-color: #dc3545;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
}

.remove-btn:hover {
  background-color: #c82333;
}

.add-route-section {
  display: flex;
  gap: 10px;
  align-items: center;
  margin-top: 15px;
}

.route-select {
  flex: 1;
  padding: 8px;
  border-radius: 8px;
  border: 1px solid #ccc;
}

.add-route-btn {
  background-color: var(--moj_zielony);
  color: white;
  border: none;
  padding: 8px 15px;
  border-radius: 8px;
  cursor: pointer;
  white-space: nowrap;
}

.add-route-btn:hover:not(:disabled) {
  background-color: #45a049;
}

.add-route-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.no-routes {
  color: #666;
  font-style: italic;
  margin: 15px 0;
}

.form-actions {
  display: flex;
  gap: 15px;
  margin-top: 30px;
}

.save-btn {
  background-color: var(--moj_zielony);
  color: white;
  border: none;
  padding: 12px 25px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
  flex: 1;
}

.save-btn:hover:not(:disabled) {
  background-color: #45a049;
}

.save-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.cancel-btn {
  background-color: #6c757d;
  color: white;
  border: none;
  padding: 12px 25px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
  flex: 1;
}

.cancel-btn:hover {
  background-color: #5a6268;
}

input, select {
  width: 100%;
  padding: 10px;
  margin: 10px 0;
  border-radius: 8px;
  border: 1px solid #ccc;
  font-size: 16px;
}

input:focus, select:focus {
  outline: none;
  border-color: #4CAF50;
}

label {
  font-size: 18px;
  color: white;
  margin-bottom: 5px;
  display: block;
}

h1 {
  color: white;
  text-align: center;
  margin-bottom: 30px;
  font-size: 28px;
}

h3 {
  color: white;
  margin-bottom: 15px;
  font-size: 20px;
}
</style>
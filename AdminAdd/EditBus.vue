<template>
  <div class="edit-bus-container">
    <h1 class="text-xl font-bold mb-4">Edytuj autobusy</h1>
    
    <!-- Lista autobusów -->
    <div v-if="!selectedBus" class="bus-list-container">
      <div v-if="loading" class="loading">
        Ładowanie autobusów...
      </div>
      
      <div v-else-if="error" class="error">
        {{ error }}
      </div>
      
      <div v-else class="bus-list">
        <div class="search-container">
          <input
            v-model="searchTerm"
            type="text"
            placeholder="Szukaj po rejestracji, marce lub modelu..."
            class="search-input"
          />
        </div>
        
        <div class="bus-grid">
          <div
            v-for="bus in filteredBuses"
            :key="bus.id"
            @click="selectBus(bus)"
            class="bus-card"
          >
            <div class="bus-info">
              <h3>{{ bus.rejestracja }}</h3>
              <p>{{ bus.marka }} {{ bus.model }}</p>
            </div>
            <button class="edit-btn">
              Edytuj
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Formularz edycji -->
    <div v-if="selectedBus" class="edit-form-container">
      <button @click="goBack" class="back-btn">
        ← Powrót do listy
      </button>
      
      <form @submit.prevent="updateBus" class="edit-form">
        <h2>Edytuj autobus: {{ originalBus.rejestracja }}</h2>
        
        <div class="form-group">
          <label for="rejestracja">Numer rejestracyjny:</label>
          <input
            id="rejestracja"
            v-model="selectedBus.rejestracja"
            type="text"
            maxlength="7"
            required
          />
        </div>

        <div class="form-group">
          <label for="marka">Marka:</label>
          <select
            id="marka"
            v-model="selectedBus.marka"
            required
          >
            <option disabled value="">Wybierz markę</option>
            <option>Mercedes</option>
            <option>MAN</option>
            <option>Solaris</option>
            <option>Volvo</option>
            <option>Scania</option>
          </select>
        </div>

        <div class="form-group">
          <label for="model">Model:</label>
          <input
            id="model"
            v-model="selectedBus.model"
            type="text"
            required
          />
        </div>

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
            @click="deleteBus"
            :disabled="deleteLoading"
            class="delete-btn"
          >
            {{ deleteLoading ? 'Usuwanie...' : 'Usuń autobus' }}
          </button>
        </div>

        <div v-if="updateError" class="error mt-2">
          {{ updateError }}
        </div>
        <div v-if="updateSuccess" class="success mt-2">
          Autobus został pomyślnie zaktualizowany!
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted} from 'vue'

// Reactive data
const buses = ref([])
const loading = ref(true)
const error = ref('')
const selectedBus = ref(null)
const originalBus = ref(null)
const searchTerm = ref('')
const updateLoading = ref(false)
const deleteLoading = ref(false)
const updateError = ref('')
const updateSuccess = ref(false)

// Computed properties
const filteredBuses = computed(() => {
  if (!searchTerm.value) return buses.value
  
  const term = searchTerm.value.toLowerCase()
  return buses.value.filter(bus => 
    bus.rejestracja.toLowerCase().includes(term) ||
    bus.marka.toLowerCase().includes(term) ||
    bus.model.toLowerCase().includes(term)
  )
})

const hasChanges = computed(() => {
  if (!selectedBus.value || !originalBus.value) return false
  
  return (
    selectedBus.value.rejestracja !== originalBus.value.rejestracja ||
    selectedBus.value.marka !== originalBus.value.marka ||
    selectedBus.value.model !== originalBus.value.model
  )
})

// Methods
const fetchBuses = async () => {
  try {
    loading.value = true
    error.value = ''
    
    const response = await $fetch('http://localhost:8000/transport/autobusy')
    buses.value = response || []
  } catch (err) {
    error.value = 'Błąd podczas pobierania autobusów'
    console.error('Błąd pobierania autobusów:', err)
  } finally {
    loading.value = false
  }
}

const selectBus = (bus) => {
  selectedBus.value = { ...bus }
  originalBus.value = { ...bus }
  updateError.value = ''
  updateSuccess.value = false
}

const goBack = () => {
  selectedBus.value = null
  originalBus.value = null
  updateError.value = ''
  updateSuccess.value = false
}

const resetForm = () => {
  if (originalBus.value) {
    selectedBus.value = { ...originalBus.value }
    updateError.value = ''
    updateSuccess.value = false
  }
}

const updateBus = async () => {
  try {
    updateLoading.value = true
    updateError.value = ''
    updateSuccess.value = false

    const updateData = {
      id: selectedBus.value.id,
      rejestracja: selectedBus.value.rejestracja,
      marka: selectedBus.value.marka,
      model: selectedBus.value.model
    }

    const response = await $fetch('http://localhost:8000/transport/autobusy', {
      method: 'PUT',
      body: JSON.stringify(updateData),
      headers: {
        'Content-Type': 'application/json'
      }
    })

    updateSuccess.value = true
    originalBus.value = { ...selectedBus.value }
    
    // Update the bus in the list
    const busIndex = buses.value.findIndex(b => b.id === selectedBus.value.id)
    if (busIndex !== -1) {
      buses.value[busIndex] = { ...selectedBus.value }
    }

    // Auto hide success message after 3 seconds
    setTimeout(() => {
      updateSuccess.value = false
    }, 3000)

  } catch (err) {
    if (err.data?.detail) {
      updateError.value = err.data.detail
    } else if (err.response?.status === 400) {
      updateError.value = 'Autobus o podanej rejestracji już istnieje'
    } else {
      updateError.value = 'Wystąpił błąd podczas aktualizacji autobusu'
    }
  } finally {
    updateLoading.value = false
  }
}

const deleteBus = async () => {
  if (!confirm(`Czy na pewno chcesz usunąć autobus ${selectedBus.value.rejestracja}?`)) {
    return
  }

  try {
    deleteLoading.value = true
    updateError.value = ''

    await $fetch(`http://localhost:8000/transport/autobusy/${selectedBus.value.id}`, {
      method: 'DELETE'
    })

    // Remove from local list
    buses.value = buses.value.filter(b => b.id !== selectedBus.value.id)
    
    // Go back to list
    goBack()

  } catch (err) {
    updateError.value = 'Wystąpił błąd podczas usuwania autobusu'
  } finally {
    deleteLoading.value = false
  }
}

// Lifecycle
onMounted(() => {
  fetchBuses()
})

// Watch for success message to auto-hide
watch(updateSuccess, (newValue) => {
  if (newValue) {
    setTimeout(() => {
      updateSuccess.value = false
    }, 3000)
  }
})
</script>

<style scoped>
.edit-bus-container {
  background-color: var(--moj_srodek);
  border-radius: 15px;
  padding: 20px;
  max-width: 1000px;

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

.bus-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 15px;
}

.bus-card {
  background-color: var(--moj_szary);
  border-radius: 10px;
  padding: 15px;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.bus-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.bus-info h3 {
  color: white;
  font-size: 18px;
  font-weight: bold;
  margin: 0 0 5px 0;
}

.bus-info p {
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

.form-group input,
.form-group select {
  width: 100%;
  padding: 12px;
  border-radius: 8px;
  border: 1px solid #ccc;
  font-size: 16px;
  background-color: #f9f9f9;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: var(--moj_zielony);
  box-shadow: 0 0 5px rgba(76, 175, 80, 0.3);
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
  .bus-grid {
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
}
</style>
<template>
  <form @submit.prevent="submitForm" class="p-4 max-w-md mx-auto space-y-4">
    <div class="container">
      <h1 class="text-xl font-bold mb-4">Edytuj Brygadę</h1>
      
      <!-- Brigade Selection -->
      <div v-if="!selectedBrigade">
        <label for="brigadeSelect" class="block font-semibold">Wybierz brygadę do edycji:</label>
        <select
          id="brigadeSelect"
          v-model="selectedBrigadeId"
          @change="loadBrigadeData"
          class="w-full border rounded px-3 py-2"
          required
        >
          <option value="">-- Wybierz brygadę --</option>
          <option 
            v-for="brigade in sortedBrygady" 
            :key="brigade.id" 
            :value="brigade.id"
          >
            {{ brigade.nazwa }}
          </option>
        </select>
      </div>

      <!-- Edit Form -->
      <div v-if="selectedBrigade">
        <div class="mb-4 p-2 bg-blue-100 rounded">
          <p class="text-sm">Edytujesz brygadę: <strong>{{ selectedBrigade.nazwa }}</strong></p>
          <button 
            type="button" 
            @click="resetSelection" 
            class="text-blue-600 text-sm underline"
          >
            Wybierz inną brygadę
          </button>
        </div>

        <div>
          <label for="nazwa" class="block font-semibold">Nazwa:</label>
          <input
            id="nazwa"
            v-model="brygada.nazwa"
            type="text"
            class="w-full border rounded px-3 py-2"
            maxlength="7"
            placeholder="np. ABC1234"
            required
          />
        </div>

        <button
          type="submit"
          :disabled="loading"
          class="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 disabled:bg-gray-400"
        >
          {{ loading ? 'Zapisywanie...' : 'Zapisz zmiany' }}
        </button>

        <button
          type="button"
          @click="deleteBrigade"
          :disabled="loading"
          class="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700 disabled:bg-gray-400 ml-2"
        >
          {{ loading ? 'Usuwanie...' : 'Usuń brygadę' }}
        </button>
      </div>

      <div v-if="error" class="text-red-500 mt-2">
        {{ error }}
      </div>
      <div v-if="success" class="text-green-500 mt-2">
        {{ success }}
      </div>
    </div>
  </form>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue'
import { useBrygady } from './script/useBrygady.js'

const { brygady, sortedBrygady, loading: brigadeLoading, error: brigadeError, fetchBrygady } = useBrygady()

const selectedBrigadeId = ref('')
const selectedBrigade = ref(null)
const loading = ref(false)
const error = ref('')
const success = ref('')

const brygada = reactive({
  id: null,
  nazwa: ''
})

onMounted(async () => {
  await fetchBrygady()
})

const loadBrigadeData = () => {
  if (!selectedBrigadeId.value) return
  
  const brigade = brygady.value.find(b => b.id === parseInt(selectedBrigadeId.value))
  if (brigade) {
    selectedBrigade.value = brigade
    brygada.id = brigade.id
    brygada.nazwa = brigade.nazwa
  }
}

const resetSelection = () => {
  selectedBrigade.value = null
  selectedBrigadeId.value = ''
  brygada.id = null
  brygada.nazwa = ''
  error.value = ''
  success.value = ''
}

const submitForm = async () => {
  try {
    loading.value = true
    error.value = ''
    success.value = ''

    const response = await $fetch(`http://localhost:8000/transport/brygady`, {
      method: 'PUT',
      body: JSON.stringify(brygada),
      headers: {
        'Content-Type': 'application/json'
      }
    })

    success.value = 'Brygada została pomyślnie zaktualizowana!'
    selectedBrigade.value.nazwa = brygada.nazwa
    await fetchBrygady() // Refresh the list
    
  } catch (err) {
    if (err.data?.detail) {
      error.value = err.data.detail
    } else if (err.response?.status === 400) {
      error.value = 'Brygada o podanej nazwie już istnieje'
    } else {
      error.value = 'Wystąpił błąd podczas aktualizacji brygady'
    }
    console.error('Błąd:', err)
  } finally {
    loading.value = false
  }
}

const deleteBrigade = async () => {
  if (!confirm(`Czy na pewno chcesz usunąć brygadę "${selectedBrigade.value.nazwa}"?`)) {
    return
  }

  try {
    loading.value = true
    error.value = ''
    success.value = ''

    await $fetch(`http://localhost:8000/transport/brygady/${brygada.id}`, {
      method: 'DELETE'
    })

    success.value = 'Brygada została pomyślnie usunięta!'
    await fetchBrygady() // Refresh the list
    resetSelection()
    
  } catch (err) {
    if (err.data?.detail) {
      error.value = err.data.detail
    } else {
      error.value = 'Wystąpił błąd podczas usuwania brygady'
    }
    console.error('Błąd:', err)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.container{
  background-color: var(--moj_srodek);
  border-radius: 15px;
}

form {
  transform: translateX(-50%);
  background-color: var(--moj_szary);
  padding: 20px;
  border-radius: 15px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  height: auto;
  width: 90%;
  display: flex;
  flex-direction: column;
}

input, select {
  width: 80%;
  padding: 10px;
  margin: 10px;
  border-radius: 8px;
  border: 1px solid #ccc;
  font-size: 16px;
}

button {
  width: 83%;
  padding: 10px;
  border-radius: 8px;
  border: 1px solid #ccc;
  font-size: 16px;
  height: 50px;
  margin: 5px;
}

input:focus, select:focus, button:focus {
  outline: none;
  border-color: #4CAF50;
}

button {
  color: white;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:hover:not(:disabled) {
  filter: brightness(0.9);
}

button:active {
  filter: brightness(0.8);
}

label {
  font-size: 24px;
  color: white;
}

select {
  background-color: #f9f9f9;
}

.bg-green-600 {
  background-color: var(--moj_zielony);
}

.bg-red-600 {
  background-color: #dc2626;
}
</style>
<template>
  <form @submit.prevent="submitForm">
    <div class="container">
      <h1 class="text-xl font-bold mb-4">Edytuj Przystanek</h1>
      
      <!-- Bus Stop Selection -->
      <div v-if="!selectedPrzystanek">
        <label for="przystanekSelect" class="block font-semibold">Wybierz przystanek do edycji:</label>
        <select
          id="przystanekSelect"
          v-model="selectedPrzystanekId"
          @change="loadPrzystanekData"
          class="w-full border rounded px-3 py-2"
          required
        >
          <option value="">-- Wybierz przystanek --</option>
          <option 
            v-for="stop in sortedPrzystanki" 
            :key="stop.id" 
            :value="stop.id"
          >
            {{ stop.nazwa }} ({{ stop.ulica }})
          </option>
        </select>
      </div>

      <!-- Edit Form -->
      <div v-if="selectedPrzystanek">
        <div class="mb-4 p-2 bg-blue-100 rounded">
          <p class="text-sm">Edytujesz przystanek: <strong>{{ selectedPrzystanek.nazwa }}</strong></p>
          <button 
            type="button" 
            @click="resetSelection" 
            class="text-blue-600 text-sm underline"
          >
            Wybierz inny przystanek
          </button>
        </div>

        <div>
          <label for="nazwa" class="block font-semibold">Nazwa:</label>
          <input
            id="nazwa"
            v-model="przystanek.nazwa"
            type="text"
            class="w-full border rounded px-3 py-2"
            required
            maxlength="50"
            placeholder="np. Plac Centralny"
          />
        </div>

        <div>
          <label for="longi" class="block font-semibold">Długość geograficzna:</label>
          <input
            id="longi"
            v-model="przystanek.longi"
            type="number"
            step="0.000001"
            class="w-full border rounded px-3 py-2"
            required
            placeholder="np. 50.061389"
          />
        </div>

        <div>
          <label for="lati" class="block font-semibold">Szerokość geograficzna:</label>
          <input
            id="lati"
            v-model="przystanek.lati"
            type="number"
            step="0.000001"
            class="w-full border rounded px-3 py-2"
            required
            placeholder="np. 19.938333"
          />
        </div>

        <div>
          <label for="ulica" class="block font-semibold">Ulica:</label>
          <input
            id="ulica"
            v-model="przystanek.ulica"
            type="text"
            class="w-full border rounded px-3 py-2"
            required
            maxlength="50"
            placeholder="np. Aleja Pokoju"
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
          @click="deletePrzystanek"
          :disabled="loading"
          class="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700 disabled:bg-gray-400 ml-2"
        >
          {{ loading ? 'Usuwanie...' : 'Usuń przystanek' }}
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
import { usePrzystanki } from './script/usePrzystanki.js'

const { przystanki, sortedPrzystanki, loading: przystankiLoading, error: przystankiError, fetchPrzystanki } = usePrzystanki()

const selectedPrzystanekId = ref('')
const selectedPrzystanek = ref(null)
const loading = ref(false)
const error = ref('')
const success = ref('')

const przystanek = reactive({
  id: null,
  nazwa: '',
  longi: '',
  lati: '',
  ulica: ''
})

onMounted(async () => {
  await fetchPrzystanki()
})

const loadPrzystanekData = () => {
  if (!selectedPrzystanekId.value) return
  
  const stop = przystanki.value.find(p => p.id === parseInt(selectedPrzystanekId.value))
  if (stop) {
    selectedPrzystanek.value = stop
    przystanek.id = stop.id
    przystanek.nazwa = stop.nazwa
    przystanek.longi = stop.longi
    przystanek.lati = stop.lati
    przystanek.ulica = stop.ulica
  }
}

const resetSelection = () => {
  selectedPrzystanek.value = null
  selectedPrzystanekId.value = ''
  przystanek.id = null
  przystanek.nazwa = ''
  przystanek.longi = ''
  przystanek.lati = ''
  przystanek.ulica = ''
  error.value = ''
  success.value = ''
}

const submitForm = async () => {
  try {
    loading.value = true
    error.value = ''
    success.value = ''

    // Konwersja na liczby
    const daneDoWyslania = {
      ...przystanek,
      longi: parseFloat(przystanek.longi),
      lati: parseFloat(przystanek.lati)
    }

    const response = await $fetch('http://localhost:8000/transport/przystanki', {
      method: 'PUT',
      body: JSON.stringify(daneDoWyslania),
      headers: {
        'Content-Type': 'application/json'
      }
    })

    success.value = 'Przystanek został pomyślnie zaktualizowany!'
    // Update the selected stop data
    Object.assign(selectedPrzystanek.value, {
      nazwa: przystanek.nazwa,
      longi: parseFloat(przystanek.longi),
      lati: parseFloat(przystanek.lati),
      ulica: przystanek.ulica
    })
    await fetchPrzystanki() // Refresh the list
    
  } catch (err) {
    if (err.data?.detail) {
      error.value = err.data.detail
    } else if (err.response?.status === 400) {
      error.value = 'Przystanek o tej nazwie już istnieje'
    } else {
      error.value = 'Wystąpił błąd podczas aktualizacji przystanku'
    }
    console.error('Błąd:', err)
  } finally {
    loading.value = false
  }
}

const deletePrzystanek = async () => {
  if (!confirm(`Czy na pewno chcesz usunąć przystanek "${selectedPrzystanek.value.nazwa}"?`)) {
    return
  }

  try {
    loading.value = true
    error.value = ''
    success.value = ''

    await $fetch(`http://localhost:8000/transport/przystanki/${przystanek.id}`, {
      method: 'DELETE'
    })

    success.value = 'Przystanek został pomyślnie usunięty!'
    await fetchPrzystanki() // Refresh the list
    resetSelection()
    
  } catch (err) {
    if (err.data?.detail) {
      error.value = err.data.detail
    } else {
      error.value = 'Wystąpił błąd podczas usuwania przystanku'
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
  margin-top: 10%;
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
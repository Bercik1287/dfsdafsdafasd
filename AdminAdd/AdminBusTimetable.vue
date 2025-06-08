<template>
  <form @submit.prevent="submitForm" class="p-4 max-w-md mx-auto space-y-4">
    <div class="container">
      <h1 class="text-xl font-bold mb-4">Dodaj przystanek</h1>
      
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
        class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:bg-gray-400"
      >
        {{ loading ? 'Dodawanie...' : 'Dodaj przystanek' }}
      </button>

      <div v-if="error" class="text-red-500 mt-2">
        {{ error }}
      </div>
      <div v-if="success" class="text-green-500 mt-2">
        Przystanek został pomyślnie dodany!
      </div>
    </div>
  </form>
</template>

<script setup>
import { reactive, ref } from 'vue'

const przystanek = reactive({
  nazwa: '',
  longi: '',
  lati: '',  // Zmienione z latki na lati
  ulica: ''
})

const loading = ref(false)
const error = ref('')
const success = ref(false)

const submitForm = async () => {
  try {
    loading.value = true
    error.value = ''
    success.value = false

    // Konwersja na liczby
    const daneDoWyslania = {
      ...przystanek,
      longi: parseFloat(przystanek.longi),
      lati: parseFloat(przystanek.lati)
    }

    const response = await $fetch('http://localhost:8000/transport/przystanki', {
      method: 'POST',
      body: JSON.stringify(daneDoWyslania),
      headers: {
        'Content-Type': 'application/json'
      }
    })

    success.value = true
    // Reset formularza po sukcesie
    przystanek.nazwa = ''
    przystanek.longi = ''
    przystanek.lati = ''
    przystanek.ulica = ''
    
  } catch (err) {
    if (err.data?.detail) {
      error.value = err.data.detail
    } else if (err.response?.status === 400) {
      error.value = 'Przystanek o tej nazwie już istnieje'
    } else {
      error.value = 'Wystąpił błąd podczas dodawania przystanku'
      console.error('Szczegóły błędu:', err)
    }
  } finally {
    loading.value = false
  }
}
</script>
  
  <style scoped>
  .container{
    background-color: var(--moj_srodek); /* Kolor tła kontenera */
    border-radius: 15px; /* Zaokrąglone rogi */
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

input{
  width: 80%;                         
  padding: 10px;    
  margin: 10px;                    
  border-radius: 8px;                  
  border: 1px solid #ccc;               
  font-size: 16px;                      
}

select {
    width: 85%;                          
  padding: 10px;                      
  border-radius: 8px;                   
  border: 1px solid #ccc;               
  font-size: 16px;                      
}
button{
width: 83%;                         /* Szerokość pól formularza i przycisków */
  padding: 10px;                        /* Wewnętrzne marginesy */
  border-radius: 8px;                   /* Zaokrąglone rogi */
  border: 1px solid #ccc;               /* Lekka ramka */
  font-size: 16px; 
  height: 50px;
}

input:focus, select:focus, button:focus {
  outline: none;                        /* Usuwamy domyślną ramkę przy focusu */
  border-color: #4CAF50;                /* Kolor ramki przy focusu */
}

button {
  background-color: var(--moj_zielony);            /* Kolor przycisku */
  color: white;                         /* Kolor tekstu w przycisku */
  border: none;                          /* Usuwamy ramkę */
  cursor: pointer;                      /* Kursor wskazujący na kliknięcie */
  transition: background-color 0.3s ease; /* Płynna zmiana koloru tła */
}

button:hover {
  background-color: #45a049;            /* Kolor tła przycisku po najechaniu */
}

button:active {
  background-color: #388e3c;            /* Kolor tła przycisku po kliknięciu */
}

label {
  font-size: 24px;                      /* Rozmiar czcionki dla etykiet */
  color: white;                          /* Kolor etykiet */
}

select {
  background-color: #f9f9f9;            /* Tło dla menu wyboru */
}
  </style>
  
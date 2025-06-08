<template>
  <form @submit.prevent="submitForm" class="p-4 max-w-md mx-auto space-y-4">
    <div class="container">
      <h1 class="text-xl font-bold mb-4">Dodaj Brygade: </h1>
      
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
        class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:bg-gray-400"
      >
        {{ loading ? 'Dodawanie...' : 'Dodaj brygade' }}
      </button>

      <div v-if="error" class="text-red-500 mt-2">
        {{ error }}
      </div>
      <div v-if="success" class="text-green-500 mt-2">
        Brygada został pomyślnie dodany!
      </div>
    </div>
  </form>
</template>

<script setup>
import { reactive, ref } from 'vue'

const brygada = reactive({
  nazwa: ''
})

const loading = ref(false)
const error = ref('')
const success = ref(false)

const submitForm = async () => {
  try {
    loading.value = true
    error.value = ''
    success.value = false

    const response = await $fetch('http://localhost:8000/transport/brygady', {
      method: 'POST',
      body: JSON.stringify(brygada),
      headers: {
        'Content-Type': 'application/json'
      }
    })

    success.value = true
    // Reset formularza po sukcesie
    brygada.nazwa = ''
  } catch (err) {
    if (err.data?.detail) {
      error.value = err.data.detail
    } else if (err.response?.status === 400) {
      error.value = 'Autobus o podanej rejestracji już istnieje'
    } else {
      error.value = 'Wystąpił błąd podczas dodawania autobusu'
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
    ;
  }
form {
                 /* Pozwala na pozycjonowanie poza kontenerem */                      /* Wyrównanie komponentu w poziomie */
  transform: translateX(-50%);          /* Dokładne wyśrodkowanie */
  background-color: var(--moj_szary);   /* Kolor tła formularza */
  padding: 20px;                        /* Wewnętrzne marginesy */
  border-radius: 15px;                  /* Zaokrąglone rogi formularza */
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2); /* Wyraźniejszy cień */
  height: auto;                         /* Zmieniamy wysokość, aby dopasować się do zawartości */
  width: 90%;                           /* Szerokość formularza - dostosowana do rozmiaru ekranu */
  display: flex;                        /* Używamy flexboxa do ułożenia elementów */
  flex-direction: column;               /* Układ pionowy */
                           /* Przerwa między elementami formularza */
}

input{
  width: 80%;                          /* Szerokość pól formularza i przycisków */
  padding: 10px;    
  margin: 10px;                    /* Wewnętrzne marginesy */
  border-radius: 8px;                   /* Zaokrąglone rogi */
  border: 1px solid #ccc;               /* Lekka ramka */
  font-size: 16px;                      /* Rozmiar czcionki */
}
select {
    width: 83%;                          /* Szerokość pól formularza i przycisków */
  padding: 10px;                        /* Wewnętrzne marginesy */
  border-radius: 8px;                   /* Zaokrąglone rogi */
  border: 1px solid #ccc;               /* Lekka ramka */
  font-size: 16px;                      /* Rozmiar czcionki */
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
  
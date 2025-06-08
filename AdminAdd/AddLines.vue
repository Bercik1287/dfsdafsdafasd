<template>
    <form @submit.prevent="submitForm">
      <div class="container">

        <h1>Dodaj linie</h1>
      <div>
        <label for="number" class="block font-semibold">Numer:</label><br>
        <input
          id="number"
          v-model="linia.numer"
          type="text"
          class="w-full border rounded px-3 py-2"
          required
        />
      </div>
      <div>
        <label for="kierunek" class="block font-semibold">Kierunek:</label><br>
        <input
          id="kierunek"
          v-model="linia.kierunek"
          type="text"
          class="w-full border rounded px-3 py-2"
          required
        />
      </div>
      <div>
        <label for="opis" class="block font-semibold">Opis:</label><br>
        <input
          id="opis"
          v-model="linia.opis"
          type="text"
          class="w-full border rounded px-3 py-2"
          required
        />
      </div>
  
  
      <button
        type="submit"
        :disabled="loading"
        class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:bg-gray-400"
      >
        {{ loading ? 'Dodawanie...' : 'Dodaj linie' }}
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

const linia = ref({
  numer: '',
  kierunek: '',
  opis: ''
})

const loading = ref(false)
const error = ref('')
const success = ref(false)

const submitForm = async () => {
  try {
    loading.value = true
    error.value = ''
    success.value = false

    console.log(linia.value.numer)
    console.log(linia.value)

    const response = await $fetch('http://localhost:8000/transport/linie', {
      method: 'POST',
      body: linia.value,
      headers: {
        'Content-Type': 'application/json'
      }
    })

    success.value = true
    // Reset formularza po sukcesie
    linia.numer = ''
    linia.kierunek = ''
    linia.opis = ''
    console.log(response)
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
    width: 85%;                          /* Szerokość pól formularza i przycisków */
  padding: 10px;                        /* Wewnętrzne marginesy */
  border-radius: 8px;                   /* Zaokrąglone rogi */
  border: 1px solid #ccc;               /* Lekka ramka */
  font-size: 16px;                      /* Rozmiar czcionki */
}
button{
width: 83%;    
margin-left: 0%;                      /* Szerokość pól formularza i przycisków */
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
  
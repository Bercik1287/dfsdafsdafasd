<template>
  <form @submit.prevent="submitForm" class="space-y-4">
    <!-- Godziny odjazdu -->
    <div>
      <label class="block mb-2">Godziny odjazdu:</label>
      <table class="departures-table w-full mb-2">
        <thead>
          <tr class="text-left border-b">
            <th class="p-2">Przystanek początkowy</th>
            <th class="p-2">Godzina</th>
            <th class="p-2">Akcje</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(departure, index) in departures" :key="index" class="border-b">
            <td class="p-2">
              <select 
                v-model="departure.startStopId"
                @focus="loadPrzystanki"
                class="w-full p-2 border rounded"
                required
              >
                <option value="" disabled>Wybierz przystanek</option>
                <option 
                  v-for="przystanek in sortedPrzystanki"
                  :key="'start-'+przystanek.id"
                  :value="przystanek.id"
                >
                  {{ przystanek.nazwa }} ({{ przystanek.ulica }})
                </option>
              </select>
              <span v-if="przystankiLoading" class="loading-text text-sm text-gray-500">Ładowanie...</span>
            </td>
            
            <td class="p-2">
              <input 
                v-model="departure.time" 
                type="time" 
                class="w-full p-2 border rounded"
                required
              >
            </td>

            <td class="p-2">
              <button 
                @click="removeDeparture(index)" 
                type="button"
                class="text-red-500"
                v-if="departures.length > 1"
              >
                Usuń
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      <button 
        type="button" 
        @click="addDeparture"
        class="dodajodjazd"
      >
        + Dodaj odjazd
      </button>
    </div>
<div class="contenermaly">
    <!-- Nazwa trasy -->
    <div>
      <label class="block mb-2">Nazwa trasy (opcjonalnie):</label>
      <input 
        v-model="form.nazwa" 
        type="text" 
        class="w-full p-2 border rounded"
      >
    </div>

    <!-- Kod wariantu -->
    <div>
      <label class="block mb-2">Kod wariantu:</label>
      <input 
        v-model="form.kodWariantu" 
        type="text" 
        class="w-full p-2 border rounded"
        required
      >
    </div>

    <!-- Numer linii -->
    <div>
      <label class="block mb-2">Numer linii (opcjonalnie):</label>
      <input 
        v-model="form.numerLinii" 
        type="text" 
        class="w-full p-2 border rounded"
      >
    </div>
</div>
    <!-- Komunikaty -->
    <div v-if="error" class="text-red-500">{{ error }}</div>
    <div v-if="success" class="text-green-500">Trasa została pomyślnie utworzona!</div>

    <!-- Przycisk submit -->
    <button 
      type="submit" 
      class="uttrase"
      :disabled="loading || !hasValidDepartures"
    >
      <span v-if="loading">Tworzenie...</span>
      <span v-else>Utwórz trasę</span>
    </button>
  </form>
</template>

<script setup>
import { reactive, ref, computed } from 'vue'
import { useTrasy } from './script/useTrasyAdd'
import { usePrzystanki } from './script/usePrzystanki'

const { przystanki, sortedPrzystanki, loading: loadingPrzystanki, fetchPrzystanki } = usePrzystanki()
const { createTrasa, loading, error, success } = useTrasy()

const form = reactive({
  nazwa: '',
  kodWariantu: 'T1',
  numerLinii: ''
})

const departures = ref([
  { startStopId: null, time: '' }
])

// Sprawdzenie czy są poprawne odjazdy
const hasValidDepartures = computed(() => {
  return departures.value.filter(d => d.startStopId && d.time).length > 0
})

// Unikalne przystanki z odjazdów
const uniqueStopIds = computed(() => {
  const stops = new Set()
  departures.value.forEach(d => {
    if (d.startStopId) stops.add(d.startStopId)
  })
  return Array.from(stops)
})

// Ładowanie przystanków przy pierwszym kliknięciu
const isPrzystankiLoaded = ref(false)
const loadPrzystanki = async () => {
  if (!isPrzystankiLoaded.value) {
    await fetchPrzystanki()
    isPrzystankiLoaded.value = true
  }
}

const addDeparture = () => {
  departures.value.push({
    startStopId: null,
    time: ''
  })
}

const removeDeparture = (index) => {
  departures.value.splice(index, 1)
}

const submitForm = async () => {
  try {
    // Przygotowanie danych do wysłania
    const validDepartures = departures.value.filter(d => d.startStopId && d.time)
    
    const trasaData = {
      przystanki_ids: uniqueStopIds.value,
      godziny_odjazdu: validDepartures.map(d => d.time),
      odjazdy: validDepartures.map(d => ({
        przystanek_id: d.startStopId,
        godzina: d.time
      })),
      nazwa_trasy: form.nazwa || undefined,
      kod_wariantu: form.kodWariantu,
      numer_linii: form.numerLinii || undefined
    }

    await createTrasa(trasaData)
    
    // Reset formularza po sukcesie
    if (success.value) {
      departures.value = [{ startStopId: null, time: '' }]
      form.nazwa = ''
      form.numerLinii = ''
    }
  } catch (err) {
    console.error('Błąd tworzenia trasy:', err)
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
  transform: translateX(-50%);          /* Dokładne wyśrodkowanie */
  background-color: var(--moj_szary);   /* Kolor tła formularza */
  padding: 20px;                        /* Wewnętrzne marginesy */
  border-radius: 15px;                  /* Zaokrąglone rogi formularza */
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2); /* Wyraźniejszy cień */
  height: auto;                         /* Zmieniamy wysokość, aby dopasować się do zawartości */
  width: 100%;                           /* Szerokość formularza - dostosowana do rozmiaru ekranu */
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
  font-size: 16px;   
  margin-left: -10;                   /* Rozmiar czcionki */
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
.dodajodjazd {
  margin-left: -9%; 
  width: 70%;                    /* Rozmiar czcionki */
}
.uttrase {
  margin-left: 12%;
  width: 70%;
}
.contenermaly{
  display: flex;                     /* Używamy flexboxa do ułożenia elementów */
  flex-direction: column;            /* Układ pionowy */
  margin: 20px;    
  margin-left: -4%;              /* Odstęp od góry */
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
table {
  width: 100%;                          /* Szerokość tabeli */
}


  </style>
  
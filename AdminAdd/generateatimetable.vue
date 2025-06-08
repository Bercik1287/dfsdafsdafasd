<template>

    <div class="container">
      <form>
        <h1>FORMULARZ GENEROWANIA ROZKŁADU JAZDY</h1>
        <!-- 1. Wybór linii -->
        <div class="form-section">
 <div v-if="loading">Ładowanie...</div>
    <div v-if="error" class="error">{{ error }}</div>
    
    <select 
      v-model="selectedLineId"
      @change="handleSelectChange"
      :disabled="loading || error"
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
  
        <!-- 2. Dane rozkładu -->
        <div class="form-section">
          <h2>2. Dane rozkładu</h2>
          <div class="date-inputs">
            <label>
              Data obowiązywania od:
              <input type="date">
            </label>
            <label>
              Data obowiązywania do:
              <input type="date">
            </label>
          </div>
        </div>

        <div class="form-section">
           <label>Wybierz trase:</label>
    <select
      v-model="selectedTrasyId"
      @change="handleSelectChange"
      :disabled="loading || error"
    >
      <option value="" disabled>Wybierz trase...</option>
      <option
        v-for="trasy in sortedTrasy"
        :key="trasy.id"
        :value="trasy.id"
      >
        {{ trasy.nazwa }}
      </option>
    </select>

    <div v-if="loading">Ładowanie listy tras...</div>
    <div v-if="error" class="error">{{ error }}</div>
  

        </div>
  
        <!-- 4. Przypisanie brygady -->
        <div class="form-section">
          <h2>4. Przypisanie brygady</h2>
 <label>Wybierz brygadę:</label>
    <select
      v-model="selectedBrygadaId"
      @change="handleSelectChange"
      :disabled="loading || error"
    >
      <option value="" disabled>Wybierz brygadę...</option>
      <option
        v-for="brygada in sortedBrygady"
        :key="brygada.id"
        :value="brygada.id"
      >
        {{ brygada.nazwa }}
      </option>
    </select>

    <div v-if="loading">Ładowanie listy brygad...</div>
    <div v-if="error" class="error">{{ error }}</div>
          


          <label>Wybierz Autobus:</label>
<select
  v-model="selectedBusId"
  :disabled="busLoading || busError"
>
  <option value="" disabled>Wybierz autobus...</option>
  <option
    v-for="bus in sortedBuses"
    :key="bus.id"
    :value="bus.id"
  >
    {{ bus.marka }} {{ bus.model }} ({{ bus.rejestracja }})
  </option>
</select>

<div v-if="busLoading">Ładowanie listy autobusów...</div>
<div v-if="busError" class="error">{{ busError }}</div>
          
    <label>Wybierz kierowce</label>
    <select 
      v-model="selectedKierowcaId"
      @focus="fetchKierowcy"
    >
      <option value="" disabled>Wybierz kierowcę</option>
      <option 
        v-for="kierowca in sortedKierowcy"
        :key="kierowca.id"
        :value="kierowca.id"
      >
        {{ kierowca.nazwisko }} {{ kierowca.imie }} ({{ kierowca.pesel }})
      </option>
    </select>
        </div>
  
        <button 
  type="button" 
  @click="generateSchedule"
  :disabled="loading"
>
  Generuj rozkład jazdy (PDF)
</button>
      </form>
    </div>
  </template>
<script setup>
import { ref, onMounted, computed, initCustomFormatter } from 'vue'
import { useLines } from './script/useScript'
import { usePrzystanki } from './script/usePrzystanki'
import { useBrygady } from './script/useBrygady'
import { useBus } from './script/useBus'
import { useKierowcy } from './script/useKierowcy'
import { useTrasy } from './script/useTrasy'

const emit = defineEmits(['select'])

const {
  loading: linesLoading,
  error: linesError,
  sortedLines,
  selectedLineId,
  fetchLines
} = useLines()
const { 
  sortedKierowcy, 
  loading: kierowcyLoading, 
  error: kierowcyError, 
  fetchKierowcy 
} = useKierowcy()
const selectedKierowcaId = ref(null)
const {
  przystanki: sortedPrzystanki,
  loading: przystankiLoading,
  error: przystankiError,
  fetchPrzystanki
} = usePrzystanki()

const {
  sortedBrygady,
  loading: brygadyLoading,
  error: brygadyError,
  fetchBrygady
} = useBrygady()
const { 
  sortedTrasy, 
  loading: trasyLoading, 
  error: trasyError, 
  fetchTrasy 
} = useTrasy()
const {
  buses,
  sortedBuses,
  loading: busLoading,
  error: busError,
  fetchBus
} = useBus()

const departures = ref([
  { startStopId: null, time: '', endStopId: null },
  { startStopId: null, time: '', endStopId: null },
  { startStopId: null, time: '', endStopId: null }
])

const addDeparture = () => {
  departures.value.push({
    startStopId: null,
    endStopId: null,
    time: ''
  })
}

const removeDeparture = (index) => {
  departures.value.splice(index, 1)
}

const selectedBrygadaId = ref(null)

const handleSelectChange = () => {
  const selected = sortedBrygady.value.find(
    b => b.id === selectedBrygadaId.value
  )
  emit('select', selected)
}

onMounted(async () => {
  await fetchLines()
  await fetchPrzystanki()
  await fetchBrygady()
  await fetchBus()
  await fetchKierowcy()
  await fetchTrasy()
})

const loading = computed(() =>
  linesLoading.value ||
  przystankiLoading.value ||
  brygadyLoading.value ||
  busLoading.value ||
  kierowcyLoading.value ||
  trasyLoading.value
)

const error = computed(() =>
  linesError.value ||
  przystankiError.value ||
  brygadyError.value ||
  busError.value ||
  kierowcyError.value ||
  trasyError.value
)
</script>
  <style scoped>
.container {
    position: absolute;
  background-color: var(--moj_szary);
  width: 130%;
  max-width: 800px;
  padding: 20px;
  font-family: Arial, sans-serif;
  
  /* Centrowanie kontenera */
  margin-left: 40%;
    margin-top: -150px;
  
  /* Centrowanie zawartości w kontenerze */
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
  
  h1 {
    text-align: center;
    color: #333;
    margin-bottom: 30px;
  }
  
  .form-section {
    margin-bottom: 30px;
    padding: 15px;
    background-color: #f5f5f5;
    border-radius: 5px;
  }
  
  h2 {
    margin-top: 0;
    color: #444;
    font-size: 1.2em;
  }
  
  label {
    display: block;
    margin-bottom: 15px;
    color:black;
  }
  
  input[type="text"],
  input[type="time"],
  select {
    width: 100%;
    padding: 8px;
    margin-top: 5px;
    border: 1px solid #ddd;
    border-radius: 4px;
  }
  
  .date-inputs {
    display: flex;
    gap: 20px;
  }
  
  .date-inputs label {
    flex: 1;
  }
  
  .departures-table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 15px;
  }
  
  .departures-table th,
  .departures-table td {
    padding: 10px;
    border: 1px solid #ddd;
    text-align: left;
  }
  
  .departures-table input {
    width: 100%;
    box-sizing: border-box;
  }
  
  button {
    background-color: #4CAF50;
    color: white;
    padding: 10px 15px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    margin-top: 10px;
  }
  
  button:hover {
    background-color: #45a049;
  }
  h1{
    color: white;
  }
  th{
    color:black;
  }
  </style>
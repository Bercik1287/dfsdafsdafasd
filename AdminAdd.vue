<template>
  <div class="container">
    <div class="button-container">

      <button>Dodaj pracownika</button>
      <button @click="activeComponent='AddBus'">Dodaj autobus</button>
      <button @click="activeComponent='AdminBusTimetable'">Dodaj przystanek</button>
      <button @click="activeComponent='AddLines'">Dodaj linie</button>
      <button @click="activeComponent='AddRoute'">Dodaj trase</button>
      <button @click="activeComponent='AddBrigade'">Dodaj Brygade</button>

    </div>
    <div class ="component-container">
      <component :is="currentComponent" />
    </div>
</div>
  </template>
<!---------------------------->
<script setup>
import AddBus from '~/components/AdminAdd/AddBus.vue'
import AdminBusTimetable from '~/components/AdminAdd/AdminBusTimetable.vue'
import AddLines from '~/components/AdminAdd/AddLines.vue'
import AddRoute from '~/components/AdminAdd/AddRoute.vue'
import AddBrigade from './AdminAdd/AddBrigade.vue'
import { computed, ref } from 'vue'

const activeComponent = ref(null)

const currentComponent = computed(() => {
  if (activeComponent.value === 'AddBus') return AddBus
  if (activeComponent.value === 'AdminBusTimetable') return AdminBusTimetable
  if (activeComponent.value === 'AddLines') return AddLines
  if (activeComponent.value === 'AddRoute') return AddRoute
    if (activeComponent.value === 'AddBrigade') return AddBrigade
  return null
})
</script>
<!---------------------------->
  <style scoped>
  .container{
    position: flex; /* Tworzymy kontekst do pozycjonowania absolutnego */
    padding: 20px;
  }
  .component-container {  
    position: absolute; /* Pozwala na pozycjonowanie poza kontenerem */
    top: -14%; /* Ustawiamy odległość od góry */
    left: 55%;
    right: 0;
    bottom: 0;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .button-container {
    background-color: var(--moj_srodek);
    display: flex;
    gap: 20px;
    justify-content: center;
    margin-top: 20px;
    flex-wrap: wrap;
    border-radius: 20px;
  }
  button{
    width: 40%;
  }
  .btn:hover {
    background-color: #45a049; /* Zmiana koloru przycisku przy hover */
  }
  </style>
<template>
  <div class="container">
    <div class="button-container">
      <button @click="activeComponent='AddBus'">Dodaj autobus</button>
      <button @click="activeComponent='EditBus'">Edytuj autobus</button>
      <button @click="activeComponent='AdminBusTimetable'">Dodaj przystanek</button>
      <button @click="activeComponent='EditBusStop'">Edytuj przystanek</button>
      <button @click="activeComponent='AddLines'">Dodaj linie</button>
      <button @click="activeComponent='EditLines'">Edytuj linie</button>
      <button @click="activeComponent='AddRoute'">Dodaj trase</button>
      <button @click="activeComponent='EditRoutes'">Edytuj Trase</button>
      <button @click="activeComponent='AddBrigade'">Dodaj Brygade</button>
      <button @click="activeComponent='EditBrigade'">Edytuj Brygade</button>
    </div>
        
  </div>
  <div class="component-container">
      <component :is="currentComponent" />
  </div>

</template>

<script setup>
import AddBus from '~/components/AdminAdd/AddBus.vue'
import EditBus from '~/components/AdminAdd/EditBus.vue'
import EditBrigade from '~/components/AdminAdd/EditBrigade.vue'
import EditBusStop from '~/components/AdminAdd/EditBusStop.vue'
import EditLines from '~/components/AdminAdd/EditLines.vue'
import EditRoutes from '~/components/AdminAdd/EditRoutes.vue'
import AdminBusTimetable from '~/components/AdminAdd/AdminBusTimetable.vue'
import AddLines from '~/components/AdminAdd/AddLines.vue'
import AddRoute from '~/components/AdminAdd/AddRoute.vue'
import AddBrigade from './AdminAdd/AddBrigade.vue'
import { computed, ref } from 'vue'

const activeComponent = ref(null)

const currentComponent = computed(() => {
  if (activeComponent.value === 'AddBus') return AddBus
  if (activeComponent.value === 'EditBus') return EditBus
  if (activeComponent.value === 'EditBrigade') return EditBrigade
  if (activeComponent.value === 'EditBusStop') return EditBusStop
  if (activeComponent.value === 'EditLines') return EditLines
  if (activeComponent.value === 'EditRoutes') return EditRoutes
  if (activeComponent.value === 'AdminBusTimetable') return AdminBusTimetable
  if (activeComponent.value === 'AddLines') return AddLines
  if (activeComponent.value === 'AddRoute') return AddRoute
  if (activeComponent.value === 'AddBrigade') return AddBrigade
  return null
})
</script>

<style scoped>
.container {
  padding: 20px;
  display: flex;
  flex-direction: column;
}

.component-container {  
  margin-top: -130%;
  width: 100%;
  margin-left: 170%;
}

.button-container {
  background-color: var(--moj_srodek);
  display: flex;
  gap: 15px;
  justify-content: center;
  margin-top: 20px;
  flex-wrap: wrap;
  border-radius: 20px;
  padding: 20px;
}

button {
  width: 30%; /* zmniejsz z 40% */
  min-width: 150px; /* minimalna szerokość */
  padding: 12px;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  background-color: var(--moj_zielony);
  color: white;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #45a049;
}

@media (max-width: 768px) {
  button {
    width: 90%;
  }
  
  .component-container {
    position: relative;
    top: 0;
    left: 0;
    margin-top: 20px;
  }
}
</style>
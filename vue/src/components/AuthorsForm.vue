<script setup>
import { useStoreAuthors } from '@/stores/storeAuthors'

const storeAuthors = useStoreAuthors()
</script>

<template>
  <p>Cadastrar autor:</p>
  <input placeholder="Nome"
    v-model="add_name"
    />
  <br>
  <button @click="add">Cadastrar</button>
  <br><br>
  <p>Buscar por:</p>
  <input placeholder="Nome"
    v-model="search_name" />
  <br>
  <button @click="storeAuthors.searchAuthors">Buscar</button>
</template>

<style scoped>
.mpx-12 {
  padding: 0px 12px 0px;
}

button {
  background-color: rgb(182, 182, 182);
  border: none;
  border-radius: 5px;
  padding: 5px;
  cursor: pointer;
  margin-top: 6px;
  font-weight: bold;
}
</style>
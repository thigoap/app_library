<script setup>
import { useStoreBooks } from '@/stores/storeBooks'

const storeBooks = useStoreBooks()
</script>

<template>
  <p>Cadastrar romance:</p>
  <input placeholder="Título"
    v-model="add_title" />
    <span class="mpx-12">e</span>
  <input placeholder="Ano"
    v-model="add_year"  />
  <span class="mpx-12">e</span>
  <input placeholder="Autor"
    v-model="add_author"  />
    
  <br>
  <button @click="add">Cadastrar</button>
  <br><br>
  <p>Buscar por:</p>
  <input placeholder="Título"
    v-model="search_title" />
  <span class="mpx-12">e/ou</span>
  <input placeholder="Ano"
    v-model="search_year"  />
  <br>
  <button @click="storeBooks.searchBooks">Buscar</button>
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
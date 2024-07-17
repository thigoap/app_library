<script setup>
import BooksForm from '../components/BooksForm.vue'
import BooksTable from '../components/BooksTable.vue'
import { useStoreBooks } from '@/stores/storeBooks'

const storeBooks = useStoreBooks()
</script>

<template>
  <div class="content">
    <h1>Livros</h1>
    <BooksForm />
    <br><br>
    <div v-if="storeBooks.books.length">
      <BooksTable />
    </div>
  </div>
</template>

<style>

</style>

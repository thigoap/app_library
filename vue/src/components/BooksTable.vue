<script setup>
import { useStoreBooks } from '@/stores/storeBooks'

const storeBooks = useStoreBooks()
</script>

<template>
  <table>
    <tr>
      <th>Ano</th>
      <th>Título</th>
      <th>Autor</th>
    </tr>
    <tr v-for='book in storeBooks.books'>
      <td>{{ book.year }}</td>
      <td>{{ book.title }}</td>
      <td>{{ book.author }}</td>
    </tr>
  </table>
</template>

<style scoped>
table {
  border-spacing: 0px;
}
th {
  font-weight: bold;
}
th, td {
  border: 1px solid rgb(182, 182, 182);
  padding: 0px 12px 0px;
}
</style>
<script setup>
import { useStoreAuthors } from '@/stores/storeAuthors'

const storeAuthors = useStoreAuthors()
</script>

<template>
  <table>
    <tr>
      <th>Romancista</th>
      <th>ID</th>
    </tr>
    <tr v-for='author in storeAuthors.authors'>
      <td>{{ author.name }}</td>
      <td>{{ author.id }}</td>
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
<script setup>
import AuthorsTable from '../components/AuthorsTable.vue'
import AuthorsForm from '../components/AuthorsForm.vue'
import { useStoreAuthors } from '@/stores/storeAuthors'

const storeAuthors = useStoreAuthors()
</script>

<template>
  <div class="content">
    <h1>Romancistas</h1>
    <AuthorsForm />
    <br><br>
    <AuthorsTable v-if="storeAuthors.authors.length" />
  </div>
</template>

<style>

</style>

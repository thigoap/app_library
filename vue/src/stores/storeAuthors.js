import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useStoreAuthors = defineStore('authors', () => {
  /* states */
  const authors = ref([])

  /* getters */ 

  /* actions */
  const API_URL = `http://localhost:3000/authors` /* for testing */
  
  const getPost = () => {
    return fetch(API_URL).then(response => response.json())
  }

  const addAuthor = () => {
    console.log('add')
  }
  
  const searchAuthors = () => {
    console.log('search')
    getPost().then(data => {
      authors.value = data
    })
    console.log(authors.value)
  }

  /* return */  
  return { authors, addAuthor, searchAuthors }
})
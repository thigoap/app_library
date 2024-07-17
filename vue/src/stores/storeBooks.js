import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useStoreBooks = defineStore('books', () => {
  /* states */
  const books = ref([])

  /* getters */ 

  /* actions */
  const API_URL = `http://localhost:3000/books` /* for testing */
  
  const getPost = () => {
    return fetch(API_URL).then(response => response.json())
  }

  const addBook = () => {
    console.log('add')
  }
  
  const searchBooks = () => {
    console.log('search')
    getPost().then(data => {
      books.value = data
    })
    console.log(books.value)
  }

  /* return */  
  return { books, addBook, searchBooks }
})
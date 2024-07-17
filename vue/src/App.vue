<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div class="wrapper">
    <header>
      <nav>
        <RouterLink to="/">Início</RouterLink>
        <RouterLink to="/books">Livros</RouterLink>
        <RouterLink to="/authors">Romancistas</RouterLink>
        <RouterLink to="/about">Sobre</RouterLink>
      </nav>
    </header>
    <div class="main-content">
      <RouterView />
    </div>
  </div>
</template>

<style scoped>
.wrapper {
  display: flex;
  max-width: 800px;
  margin: 0 auto;
}

nav {
  display: flex;
  flex-direction: column;
  border-right: 1px solid rgb(182, 182, 182);
  padding-right: 4px;
}

.main-content {
  padding-left: 50px;
}

@media (max-width: 600px) {
  .wrapper{
    flex-direction: column;
  }

  nav {
    flex-direction: row;
    justify-content: space-between;
    border-bottom: 1px solid rgb(182, 182, 182);
    border-right: none;
    margin-bottom: 16px;
  }

  .main-content {
  padding-left: 0px;
}
}

</style>

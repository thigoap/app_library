<script setup>

</script>

<template>
  <p>Cadastre-se:</p>
  <input placeholder="Nome de usuário"
    v-model="username" /><br>
  <input placeholder="Email"
    v-model="email"  /><br>
  <input placeholder="Senha"
    v-model="password"  />
  <br>
  <button @click="add">Cadastrar</button>
  <br><br>
  <p>Ou acesse:</p>
  <input placeholder="Nome de usuário"
    v-model="username" /><br>
  <input placeholder="Senha"
    v-model="password"  />
  <br>
  <button @click="add">Login</button>
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
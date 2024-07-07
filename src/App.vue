<script setup lang="ts">
// You don't need to import these manually
// import { ref } from 'vue'
// import HelloWorld from './components/HelloWorld.vue'

const message = ref('')

const showMsg = async () => {
    const response = await fetch('http://127.0.0.1:8000', { 
      credentials: 'include' // for google's IDX only.
    })
    const data = await response.json()
    message.value = data.message
}

</script>

<template>
  <div>
      
      <button @click="showMsg">Show Message</button>
      <h1 v-if="message.hello">{{ $t('message.hello') }}</h1>

      <nav>
      <RouterLink to="/">Home</RouterLink> | 
      <RouterLink to="/about">About</RouterLink>
    </nav>
    <HelloWorld :msg="message" />
  </div>
</template>

<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>

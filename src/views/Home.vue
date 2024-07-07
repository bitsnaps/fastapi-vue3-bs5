<script setup>
import { useHead } from '@unhead/vue'
import { useLocalStorage } from '@vueuse/core'

useHead({
  title: 'Home',
  meta: [
    { name: 'description', content: 'Welcome to the Vue 3 Home Page.' },
  ],
})

// persist state in localStorage
const store = useLocalStorage('token', {username: ''})

</script>

<template>
  <div class="home">
    <h1>Home</h1>
    <p>Welcome to the Vue 3 Home Page.</p>
  </div>
</template>
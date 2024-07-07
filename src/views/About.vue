<script setup>
import { useHead } from '@unhead/vue'

useHead({
  title: 'About',
  meta: [
    { name: 'description', content: 'Learn more about us.' },
  ],
})
</script>


<template>
  <div class="about">
    <h1>This is an about page</h1>
  </div>
</template>
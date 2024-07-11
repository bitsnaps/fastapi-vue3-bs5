<script setup lang="ts">
import { ref } from 'vue'
import { useLocalStorage } from '@vueuse/core'

// persist state in localStorage
const store = useLocalStorage('token', { username: '' })

</script>

<template>
  <div class="container-fluid h-100 d-flex flex-column">

    <div class="row flex-grow-1">
      <ChatMessages />

      <ChatMessage />

    </div><!-- .row -->
  </div>
</template>
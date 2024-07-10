<script setup lang="ts">
import { ref } from 'vue'
import { formatDate } from '@vueuse/core'
const message = ref('')


const postRequest = async () => {

  try {
    // fetch request using POST
    const response = await fetch(`${import.meta.env.VITE_API_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        "message": 'Tell me a joke.'
      })
    })

    if (response.ok) {
      const data = await response.json()
      if (data) {
        message.value = `${data.message} at: ${formatDate(new Date(), 'HH:mm:ss')}`
      } else {
        message.value = 'error'
      }
    }
  } catch (e) {
    message.value = `${e} at: ${formatDate(new Date(), 'HH:mm:ss')}`
  }
}

const showMsg = async () => {
  const response = await fetch(`${import.meta.env.VITE_API_URL}`)
  const data = await response.json()
  message.value = data.message
}

</script>

<template>
  <div>

    <BButton variant="primary" @click="postRequest">Chat</BButton>

    <BButton variant="success" @click="showMsg">Show message</BButton>

    <h1 v-if="message">{{ message }}</h1>

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
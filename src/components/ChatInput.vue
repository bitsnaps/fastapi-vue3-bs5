<script setup lang="ts">
import { useToast } from 'bootstrap-vue-next'

//const { show } = useToast()

const sendMessage = async () => {
  try {

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
      alert(data.message)
    }
  } catch (e) {
    console.error(e)
  }

}

</script>

<template>
  <div class="p-3 bg-white border-top">
    <form class="d-flex" @submit.prevent="sendMessage">
      <input type="text" class="form-control me-2" placeholder="Type your message...">
      <BButton type="submit" variant="info"> Send </BButton>
    </form>
  </div>
</template >
      
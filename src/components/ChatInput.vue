<script setup lang="ts">
import { ref } from 'vue'
import { useApi } from '../services/api.ts'
import { Message } from '../types'
import { useMessagesStore } from '../store'
const { addUserMessage, addSystemMessage, isMessageValid } = useApi()

//import { useToast } from 'bootstrap-vue-next'

//const { show } = useToast()

const message = ref('')
const prompt = ref('')


const messagesStore = useMessagesStore()

// Create some dummy messages:
messagesStore.messages.push({ role: 'user', content: 'Hello!' })
messagesStore.messages.push({
  role: 'system', content: `**Hi**

there! How can I help you today?` })

const sendMessage = async () => {

  messagesStore.messages.push({
    role: 'user',
    content: prompt.value
  })

  const answer = await addSystemMessage(prompt.value)
  if (answer) {
    messagesStore.messages.push({
      role: "system",
      content: answer
    });
    message.value = answer
    prompt.value = ''
  }
}

const clearMessages = () => {
  messagesStore.messages.splice(0, messagesStore.messages.length)
}

</script>

<template>
  <div class="p-3 bg-white border-top">
    <form class="d-flex" @submit.prevent="sendMessage">
      <BFormInput v-model="prompt" placeholder="Type your message..." class="me-2" />
      <BButton variant="warning" class="me-1" @click="clearMessages"> Clear </BButton>
      <BButton type="submit" variant="info" :disabled="!isMessageValid(prompt)"> Send </BButton>
    </form>
  </div>
</template >
      
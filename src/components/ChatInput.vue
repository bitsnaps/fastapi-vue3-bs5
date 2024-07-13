<script setup lang="ts">
import { ref } from 'vue'
import { useApi } from '../services/api.ts'
import { Message } from '../types'
import { useMessagesStore } from '../store'
import { BFormCheckbox } from 'bootstrap-vue-next';
const { addSystemMessage, isMessageValid } = useApi()

//import { useToast } from 'bootstrap-vue-next'

//const { show } = useToast()

const message = ref('')
const prompt = ref('')
const useAgents = ref(false)
const streamResponse = ref(false)

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

  const answer = await addSystemMessage(prompt.value.trim(), useAgents.value, streamResponse.value)
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
    <div class="row">
      <div class="col-md-12">

        <form class="d-flex" @submit.prevent="sendMessage">
          <BFormInput v-model="prompt" placeholder="Type your message..." class="me-2" />
          <BButton variant="warning" class="me-1" @click="clearMessages"> Clear </BButton>
          <BButton type="submit" variant="info" :disabled="!isMessageValid(prompt)"> Send </BButton>
        </form>

      </div><!-- .col -->
      <div class="col md-12 mt-2 d-flex flex-row justify-content-start">
        <BFormCheckbox v-model="useAgents">Use Agents</BFormCheckbox>
        <BFormCheckbox class="ms-1" v-model="streamResponse">Stream</BFormCheckbox>

      </div>

    </div>
  </div>
</template >
      
<script setup lang="ts">
import { useMessagesStore } from '../store'

const messagesStore = useMessagesStore()

</script>

<template>
  <div class="col-md-9 d-flex flex-column">

    <div class="chat-list flex-grow-1 p-3 overflow-auto">

      <div v-for="message in messagesStore.messages" :key="JSON.stringify(message)">

        <UserMessage v-if="message['role'] == 'user'" :message="message['content']" />

        <AIMessage v-if="message['role'] == 'system'" :message="message['content']" />

      </div>

      <!-- AIMessage message="Hello! How can I help you today?" / -->

      <!-- UserMessage message="I'd like to know more about artificial intelligence.Can you explain it to me ?" / -->

      <!-- AIMessage message="Certainly! Artificial Intelligence (AI) refers to the development of computer systems
        that can perform tasks that typically require human intelligence. These tasks include learning,
        problem-solving, perception, and language understanding. AI systems are designed to analyze data,
        recognize patterns, and make decisions or predictions based on that information." /-->

    </div> <!-- . flex-grow -->

    <ChatInput />

  </div><!-- .col -->
</template>


<style scoped>
div.chat-list {
  height: calc(100vh - 100px);
}
</style>
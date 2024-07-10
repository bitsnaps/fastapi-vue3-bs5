<script setup lang="ts">
import { ref } from 'vue'
import { useLocalStorage } from '@vueuse/core'

// persist state in localStorage
const store = useLocalStorage('token', { username: '' })

const chats = ref<{ id: number, message: string }[]>([
  //{ id: 1, message: 'chat 01' }
])

</script>

<template>
  <div class="container-fluid h-100 d-flex flex-column">

    <div class="row flex-grow-1">

      <div class="col-md-3 bg-dark text-light p-3 d-none d-md-block">
        <h3 class="mb-4">Chat History</h3>
        <ul class="list-unstyled" v-for="chat in chats" :key="chat?.id">
          <li class="mb-2">
            <a href="#" class="text-light">{{ chat?.message }}</a>
          </li>
        </ul>
        <button class="btn btn-outline-light mt-4 w-100">New Chat</button>
      </div><!-- .col -->

      <div class="col-md-9 d-flex flex-column">
        <div class="flex-grow-1 p-3 overflow-auto" style="height: calc(100vh - 100px);">
          <div class="mb-3">
            <div class="d-flex">
              <div class="rounded-circle bg-primary text-white p-2 me-2"
                style="width: 40px; height: 40px; display: flex; align-items: center; justify-content: center;">U</div>
              <div class="bg-white p-3 rounded shadow-sm" style="max-width: 80%;">
                <p class="mb-0">Hello! How can I help you today?</p>
              </div>
            </div>
          </div>

          <div class="mb-3">
            <div class="d-flex justify-content-end">
              <div class="bg-primary text-white p-3 rounded shadow-sm" style="max-width: 80%;">
                <p class="mb-0">I'd like to know more about artificial intelligence. Can you explain it to me?</p>
              </div>
              <div class="rounded-circle bg-secondary text-white p-2 ms-2"
                style="width: 40px; height: 40px; display: flex; align-items: center; justify-content: center;">A</div>
            </div>
          </div>

          <div class="mb-3">
            <div class="d-flex">
              <div class="rounded-circle bg-primary text-white p-2 me-2"
                style="width: 40px; height: 40px; display: flex; align-items: center; justify-content: center;">U</div>
              <div class="bg-white p-3 rounded shadow-sm" style="max-width: 80%;">
                <p class="mb-0">Certainly! Artificial Intelligence (AI) refers to the development of computer systems
                  that can perform tasks that typically require human intelligence. These tasks include learning,
                  problem-solving, perception, and language understanding. AI systems are designed to analyze data,
                  recognize patterns, and make decisions or predictions based on that information.</p>
              </div>
            </div>
          </div>
        </div>
        <div class="p-3 bg-white border-top">
          <form class="d-flex">
            <input type="text" class="form-control me-2" placeholder="Type your message...">
            <button type="submit" class="btn btn-primary">Send</button>
          </form>
        </div>
      </div><!-- .col -->

    </div><!-- .row -->
  </div>
</template>
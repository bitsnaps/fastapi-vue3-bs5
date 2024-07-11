<script setup lang="ts">
import { ref } from 'vue'

//defineProps<{ chats?: string }>()

const chats = ref<{ id: number, message: string }[]>([
  //{ id: 1, message: 'chat 01' }
])

</script>

<template>
  <div class="col-md-3 bg-dark text-light p-3 d-none d-md-block">
    <h3 class="mb-4">Chat History</h3>
    <ul class="list-unstyled" v-for="chat in chats" :key="chat?.id">
      <li class="mb-2">
        <a href="#" class="text-light">{{ chat?.message }}</a>
      </li>
    </ul>
    <button class="btn btn-outline-light mt-4 w-100">New Chat</button>
  </div><!-- .col -->
</template>

<style scoped></style>

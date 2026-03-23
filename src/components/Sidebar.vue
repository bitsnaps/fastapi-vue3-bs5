<script setup lang="ts">
import { BButton, BCol } from 'bootstrap-vue-next';
import llm from '../services/llm'
import { ref } from 'vue'

const prompt = ref('')
const output = ref('')

const sendQuery = async () => {
    let payload = {"id": 1, "prompt": prompt.value };
    console.log(payload);
    
    const response = await fetch('http://127.0.0.1:8000/chat', { 
      method: 'POST',
      // headers: {
      //       'Content-Type': 'application/json'
      // },
      body: JSON.stringify(payload),
      credentials: 'include' // for google's IDX only.
    })
    const data = await response.json()
    output.value = data.message
}
</script>

<template>
  <div class="row">

    <BForm @submit.prevent="sendQuery">
      <BInput id="query" placeholder="Input your query" v-model="prompt"/>
      <BButton variant="primary" type="submit">Query</BButton>
    </BForm>

    <BCol cols="auto">
      <p>{{ output }}</p>
    </BCol>
  </div>
</template>

<style scoped>

</style>

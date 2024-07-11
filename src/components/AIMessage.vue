<script setup lang="ts">
defineProps<{ message: string }>()

</script>

<template>
  <div class="mb-3">
    <div class="d-flex">
      <ProfileIcon letter="A" variant="primary" />
      <div class="bg-white p-3 rounded shadow-sm" style="max-width: 80%;">
        <p class="mb-0">{{ message }}</p>
      </div>
    </div>
  </div>
</template>
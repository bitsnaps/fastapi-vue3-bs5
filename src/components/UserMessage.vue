<script setup lang="ts">
defineProps<{ message: string }>()

</script>

<template>
  <div class="mb-3">
    <div class="d-flex justify-content-end">
      <div class="bg-primary text-white p-3 rounded shadow-sm" style="max-width: 80%;">
        <p class="mb-0">{{ message }}</p>
      </div>
      <ProfileIcon letter="U" variant="secondary" />
    </div>
  </div>
</template>
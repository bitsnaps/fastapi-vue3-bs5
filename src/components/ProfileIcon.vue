<script setup lang="ts">
defineProps<{ letter: string, variant: string }>()
</script>
<template>
  <div :class="`profile-icon rounded-circle bg-${variant} text-white p-2 me-2`">{{ letter }}</div>
</template>

<style scoped>
div.profile-icon {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
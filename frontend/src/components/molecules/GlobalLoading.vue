<script lang="ts">
import { defineComponent } from 'vue'
export default defineComponent({})
</script>

<template>
  <div class="fixed inset-0 bg-gray-100 bg-opacity-60 transition-opacity z-50">
    <div className="flex justify-center h-screen w-screen items-center">
      <div
        className="animate-spin h-10 w-10 border-4 border-blue-500 rounded-full border-t-transparent"
      ></div>
    </div>
  </div>
</template>

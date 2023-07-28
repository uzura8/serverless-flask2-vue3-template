<script lang="ts">
import { defineComponent } from 'vue'
export default defineComponent({
  props: {
    isFullscreen: {
      type: Boolean,
      default: false
    }
  }
})
</script>

<template>
  <div
    class="bg-gray-100 bg-opacity-60 transition-opacity z-50"
    :class="{ 'fixed inset-0': isFullscreen }"
  >
    <div
      class="flex justify-center h-screen w-screen items-center"
      :class="{ 'h-screen w-screen': isFullscreen }"
    >
      <div
        class="animate-spin h-10 w-10 border-4 border-blue-500 rounded-full border-t-transparent"
      ></div>
    </div>
  </div>
</template>

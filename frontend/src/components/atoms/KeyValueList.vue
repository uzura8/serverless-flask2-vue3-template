<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  components: {},

  props: {
    items: {
      type: Object,
      required: true
    }
  },

  setup() {
    return {}
  }
})
</script>

<template>
  <dl class="space-y-4">
    <div
      v-for="(item, idx) in items"
      :key="idx"
      class="flex justify-start items-start"
    >
      <dt class="text-gray-500 min-w-150 flex-shrink-0 mr-4">{{ item.label }}</dt>
      <dd class="text-gray-900 flex-grow break-all">{{ item.value }}</dd>
    </div>
  </dl>
</template>

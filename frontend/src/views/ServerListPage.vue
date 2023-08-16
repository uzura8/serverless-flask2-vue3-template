<script lang="ts">
import { defineComponent } from 'vue'
import ServerList from '@/components/organisms/ServerList.vue'

export default defineComponent({
  components: {
    ServerList
  },

  props: {},

  setup() {
    return {}
  }
})
</script>

<template>
  <h1 class="mb-12 text-2xl font-extrabold dark:text-white">{{ $t('pgit.term.serverList') }}</h1>
  <ServerList class="mt-12" />
</template>

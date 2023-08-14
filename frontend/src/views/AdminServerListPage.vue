<script lang="ts">
import { defineComponent } from 'vue'
import AdminServerList from '@/components/organisms/AdminServerList.vue'

export default defineComponent({
  components: {
    AdminServerList
  },

  props: {},

  setup() {
    return {}
  }
})
</script>

<template>
  <h1 class="mb-12 text-2xl font-extrabold dark:text-white">{{ $t('pgit.term.serverList') }}</h1>
  <AdminServerList class="mt-12" />
</template>

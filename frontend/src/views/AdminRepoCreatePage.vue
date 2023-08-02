<script lang="ts">
import { defineComponent } from 'vue'
import AdminRepoForm from '@/components/organisms/AdminRepoForm.vue'

export default defineComponent({
  components: { AdminRepoForm },

  props: {},

  setup() {
    return {}
  }
})
</script>

<template>
  <h1 class="mb-12 text-2xl font-semibold dark:text-white">
    {{ $t('common.addFor', { target: $t('pgit.term.repository') }) }}
  </h1>

  <AdminRepoForm />
</template>

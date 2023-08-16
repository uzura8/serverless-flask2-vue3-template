<script lang="ts">
import { defineComponent } from 'vue'
import RepoForm from '@/components/organisms/RepoForm.vue'

export default defineComponent({
  components: { RepoForm },

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

  <RepoForm />
</template>

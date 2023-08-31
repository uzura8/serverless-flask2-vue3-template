<script lang="ts">
import { defineComponent, computed } from 'vue'
import { useRoute } from 'vue-router'
import RepoForm from '@/components/organisms/RepoForm.vue'

export default defineComponent({
  components: { RepoForm },

  props: {},

  setup() {
    const route = useRoute()
    const repoId = computed(() => {
      if (typeof route.params.repoId !== 'string') ''
      return route.params.repoId
    })

    return {
      repoId
    }
  }
})
</script>

<template>
  <h1 class="mb-12 text-2xl font-semibold dark:text-white">
    {{ $t('common.editOf', { label: $t('pgit.term.repository') }) }}
  </h1>

  <RepoForm :repo-id="repoId" />
</template>

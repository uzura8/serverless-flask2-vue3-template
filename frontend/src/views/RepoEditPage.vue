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
      if (route.params.repoId == null) return ''
      if (Array.isArray(route.params.repoId)) return route.params.repoId[0]
      return route.params.repoId
    })

    return {
      repoId
    }
  }
})
</script>

<template>
  <h1 class="text-2xl font-semibold dark:text-white">
    {{ $t('common.editOf', { label: $t('pgit.term.repository') }) }}
  </h1>

  <RepoForm
    class="mt-12"
    :repo-id="repoId"
  />
</template>

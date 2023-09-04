<script lang="ts">
import { defineComponent, computed } from 'vue'
import { useRoute } from 'vue-router'
import BranchList from '@/components/organisms/BranchList.vue'

export default defineComponent({
  components: {
    BranchList
  },

  props: {},

  setup() {
    const route = useRoute()
    const serverDomain = computed(() => {
      if (typeof route.params.serverDomain !== 'string') {
        throw new Error('serverDomain is not string')
      }
      return route.params.serverDomain
    })

    const repoId = computed(() => {
      if (typeof route.params.repoId !== 'string') {
        throw new Error('Repository ID is not string')
      }
      return route.params.repoId
    })

    return {
      serverDomain,
      repoId
    }
  }
})
</script>

<template>
  <div>
    <RouterLink
      :to="`/servers/${serverDomain}/repositories`"
      class="font-medium text-blue-600 dark:text-blue-500 hover:underline"
    >
      <FontAwesomeIcon icon="chevron-left" />
      {{ $t('pgit.term.repositoryList') }}
    </RouterLink>
  </div>

  <h1 class="mt-12 text-2xl font-semibold dark:text-white">
    {{ $t('pgit.term.branchList') }}
  </h1>
  <h2 class="mt-2 text-xl font-medium text-gray-500 dark:text-gray-400">
    <span class="text-base font-medium">RepositoryID:</span>
    <span class="ml-2">{{ repoId }}</span>
  </h2>
  <BranchList
    class="mt-12"
    :repo-id="repoId"
  />
</template>

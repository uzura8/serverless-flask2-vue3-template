<script lang="ts">
import { defineComponent, computed } from 'vue'
import { useRoute } from 'vue-router'
import JobList from '@/components/organisms/JobList.vue'

export default defineComponent({
  components: {
    JobList
  },

  props: {},

  setup() {
    const route = useRoute()
    const repoId = computed(() => {
      if (typeof route.params.repoId !== 'string') {
        throw new Error('Repository ID is not string')
      }
      return route.params.repoId
    })

    return {
      repoId
    }
  }
})
</script>

<template>
  <div>
    <RouterLink
      to="/repositories"
      class="font-medium text-primary-600 dark:text-primary-500 hover:underline"
    >
      <FontAwesomeIcon icon="chevron-left" />
      {{ $t('pgit.term.repositoryList') }}
    </RouterLink>
  </div>
  <h1 class="mt-12 text-2xl font-semibold dark:text-white">{{ $t('pgit.term.jobList') }}</h1>
  <h2 class="mt-2 text-xl font-medium text-gray-500 dark:text-gray-400">
    <span class="text-base font-medium">RepositoryID:</span>
    <span class="ml-2">{{ repoId }}</span>
  </h2>
  <JobList
    class="mt-12"
    :repo-id="repoId"
  />
</template>

<script lang="ts">
import type { Repository } from '@/types/Repository'
import { defineComponent, ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import JobList from '@/components/organisms/JobList.vue'

export default defineComponent({
  components: {
    JobList
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

    const repository = ref<Repository | null>(null)
    const setRepository = (repo: Repository) => {
      if (repo === null) return
      repository.value = repo
    }
    const repoIdentifier = computed(() => {
      if (repository.value === null) return ''
      return `${repository.value.serviceDomain}/${repository.value.serviceSegment}/${repository.value.repoName}`
    })

    return {
      serverDomain,
      repoId,
      repoIdentifier,
      setRepository
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
    {{ $t('pgit.term.jobList') }}
  </h1>
  <h2 class="mt-2 text-xl font-medium text-gray-500 dark:text-gray-400">
    <span v-if="repoIdentifier">{{ repoIdentifier }}</span>
    <span v-else>
      <span class="text-base font-medium">RepositoryID:</span>
      <span class="ml-2">{{ repoId }}</span>
    </span>
  </h2>
  <JobList
    class="mt-12"
    :repo-id="repoId"
    @loaded-repository="setRepository"
  />
</template>

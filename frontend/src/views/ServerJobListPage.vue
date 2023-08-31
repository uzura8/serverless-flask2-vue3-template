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
    const serverDomain = computed(() => {
      if (typeof route.params.serverDomain !== 'string') {
        throw new Error('serverDomain is not string')
      }
      return route.params.serverDomain
    })

    return {
      serverDomain
    }
  }
})
</script>

<template>
  <div>
    <RouterLink
      to="/servers"
      class="font-medium text-primary-600 dark:text-primary-500 hover:underline"
    >
      <FontAwesomeIcon icon="chevron-left" />
      {{ $t('pgit.term.serverList') }}
    </RouterLink>
  </div>
  <h1 class="mt-12 text-2xl font-semibold dark:text-white">{{ $t('pgit.term.jobList') }}</h1>
  <h2 class="mt-2 text-xl font-medium text-gray-500 dark:text-gray-400">{{ serverDomain }}</h2>
  <JobList
    class="mt-12"
    :server-domain="serverDomain"
  />
</template>

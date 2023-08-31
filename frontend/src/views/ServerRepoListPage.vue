<script lang="ts">
import { defineComponent, computed } from 'vue'
import { useRoute } from 'vue-router'
import RepoList from '@/components/organisms/RepoList.vue'

export default defineComponent({
  components: {
    RepoList
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
      class="font-medium text-blue-600 dark:text-blue-500 hover:underline"
    >
      <FontAwesomeIcon icon="chevron-left" />
      {{ $t('pgit.term.serverList') }}
    </RouterLink>
  </div>

  <h1 class="mt-12 text-2xl font-semibold dark:text-white">{{ $t('pgit.term.repositoryList') }}</h1>
  <h2 class="mt-2 text-xl font-medium text-gray-500 dark:text-gray-400">{{ serverDomain }}</h2>

  <RouterLink
    :to="`/servers/${serverDomain}/repositories/create`"
    type="button"
    class="inline-block mt-12 text-gray-900 bg-white border border-gray-300 focus:outline-none hover:bg-gray-100 focus:ring-4 focus:ring-gray-200 font-medium rounded-lg text-sm px-5 py-2.5 mr-2 mb-2 dark:bg-gray-800 dark:text-white dark:border-gray-600 dark:hover:bg-gray-700 dark:hover:border-gray-600 dark:focus:ring-gray-700"
  >
    <FontAwesomeIcon
      class="mr-2"
      icon="plus"
    />
    {{ $t('common.addFor', { target: $t('pgit.term.repository') }) }}
  </RouterLink>

  <RepoList
    class="mt-8"
    :server-domain="serverDomain"
  />
</template>

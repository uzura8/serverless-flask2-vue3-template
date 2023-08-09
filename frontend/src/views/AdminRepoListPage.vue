<script lang="ts">
import { defineComponent } from 'vue'
import AdminRepoList from '@/components/organisms/AdminRepoList.vue'

export default defineComponent({
  components: {
    AdminRepoList
  },

  props: {},

  setup() {
    return {}
  }
})
</script>

<template>
  <h1 class="mb-12 text-2xl font-semibold dark:text-white">{{ $t('pgit.term.repositoryList') }}</h1>
  <div>
    <RouterLink
      to="/admin/repositories/create"
      type="button"
      class="text-gray-900 bg-white border border-gray-300 focus:outline-none hover:bg-gray-100 focus:ring-4 focus:ring-gray-200 font-medium rounded-lg text-sm px-5 py-2.5 mr-2 mb-2 dark:bg-gray-800 dark:text-white dark:border-gray-600 dark:hover:bg-gray-700 dark:hover:border-gray-600 dark:focus:ring-gray-700"
    >
      <FontAwesomeIcon
        class="mr-2"
        icon="plus"
      />
      {{ $t('common.addFor', { target: $t('pgit.term.repository') }) }}
    </RouterLink>

    <AdminRepoList class="mt-12" />
  </div>
</template>

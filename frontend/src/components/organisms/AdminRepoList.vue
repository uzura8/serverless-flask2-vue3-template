<script lang="ts">
import type { Repository } from '@/types/Repository'
import { defineComponent, ref, onBeforeMount } from 'vue'
import { useAdminUserStore } from '@/stores/adminUser'
import { useGlobalLoaderStore } from '@/stores/globalLoader.js'
import { AdminRepositoryApi } from '@/apis'
import AdminRepoListItem from '@/components/molecules/AdminRepoListItem.vue'

export default defineComponent({
  components: { AdminRepoListItem },

  setup() {
    const adminUser = useAdminUserStore()
    const globalLoader = useGlobalLoaderStore()

    const repos = ref<Repository[]>([])
    const setRepos = async () => {
      try {
        globalLoader.updateLoading(true)
        const res = await AdminRepositoryApi.getList(null, adminUser.idToken)
        repos.value = res.items
        globalLoader.updateLoading(false)
      } catch (error) {
        console.error(error)
        globalLoader.updateLoading(false)
      }
    }

    onBeforeMount(async () => {
      await setRepos()
    })

    return {
      repos
    }
  }
})
</script>

<template>
  <div>
    <p v-if="repos.length === 0">
      {{ $t('msg.dataIsEmpty') }}
    </p>
    <div
      v-else
      class="overflow-x-auto"
    >
      <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
        <thead
          class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400"
        >
          <tr>
            <th
              scope="col"
              class="px-4 py-3"
            >
              {{ $t('pgit.term.deployStatus') }}
            </th>
            <th
              scope="col"
              class="px-4 py-3"
            >
              {{ $t('pgit.term.server') }}
            </th>
            <th
              scope="col"
              class="px-4 py-3"
            >
              {{ $t('pgit.form.repository.service') }}
            </th>
            <th
              scope="col"
              class="px-4 py-3"
            >
              {{ $t('pgit.form.repository.serviceSegment') }}
            </th>
            <th
              scope="col"
              class="px-4 py-3"
            >
              {{ $t('pgit.form.repository.repoName') }}
            </th>
            <th
              scope="col"
              class="px-4 py-3"
            >
              {{ $t('pgit.form.repository.buildType') }}
            </th>
            <th
              scope="col"
              class="px-4 py-3"
            >
              <span class="sr-only">Actions</span>
            </th>
          </tr>
        </thead>
        <tbody>
          <AdminRepoListItem
            v-for="repo in repos"
            :key="repo.repoId"
            :repo="repo"
          />
        </tbody>
      </table>
    </div>
  </div>
</template>

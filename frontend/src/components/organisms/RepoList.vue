<script lang="ts">
import type { Repository } from '@/types/Repository'
import { defineComponent, ref, onBeforeMount } from 'vue'
import { storeToRefs } from 'pinia'
import { useUserStore } from '@/stores/user'
import { useGlobalLoaderStore } from '@/stores/globalLoader.js'
import { RepositoryApi } from '@/apis'
import RepoListItem from '@/components/molecules/RepoListItem.vue'

export default defineComponent({
  components: { RepoListItem },

  setup() {
    const globalLoader = useGlobalLoaderStore()

    const userStore = useUserStore()
    const { idToken } = storeToRefs(userStore)

    const repos = ref<Repository[]>([])
    const setRepos = async () => {
      try {
        globalLoader.updateLoading(true)
        const res = await RepositoryApi.getList(null, idToken.value)
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
          <RepoListItem
            v-for="repo in repos"
            :key="repo.repoId"
            :repo="repo"
          />
        </tbody>
      </table>
    </div>
  </div>
</template>

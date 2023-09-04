<script lang="ts">
import type { Branch } from '@/types/Branch'
import { defineComponent, ref, onBeforeMount } from 'vue'
import { storeToRefs } from 'pinia'
import { useUserStore } from '@/stores/user'
import { useGlobalLoaderStore } from '@/stores/globalLoader.js'
import { BranchApi, RepositoryApi } from '@/apis'
import BranchListItem from '@/components/molecules/BranchListItem.vue'

export default defineComponent({
  components: { BranchListItem },

  props: {
    serverDomain: {
      type: String as () => string | null,
      required: false
    },
    repoId: {
      type: String as () => string | null,
      required: false
    }
  },

  setup(props) {
    const globalLoader = useGlobalLoaderStore()

    const userStore = useUserStore()
    const { idToken } = storeToRefs(userStore)

    const branches = ref<Branch[]>([])
    const setBranches = async () => {
      try {
        globalLoader.updateLoading(true)
        const params = { order: 'desc' }
        let res
        if (props.repoId) {
          res = await RepositoryApi.getBranches(props.repoId, params, idToken.value)
        } else {
          res = await BranchApi.getList(params, idToken.value)
        }
        branches.value = res.items
        globalLoader.updateLoading(false)
      } catch (error) {
        console.error(error)
        globalLoader.updateLoading(false)
      }
    }

    onBeforeMount(async () => {
      await setBranches()
    })

    return {
      branches
    }
  }
})
</script>

<template>
  <div>
    <p v-if="branches.length === 0">
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
              {{ $t('pgit.term.server') }}
            </th>
            <th
              scope="col"
              class="px-4 py-3"
            >
              {{ $t('pgit.term.repository') }}
            </th>
            <th
              scope="col"
              class="px-4 py-3"
            >
              {{ $t('pgit.term.branch') }}
            </th>
            <th
              scope="col"
              class="px-4 py-3"
            >
              {{ $t('common.preview') }}
            </th>
            <th
              scope="col"
              class="px-4 py-3"
            >
              {{ $t('pgit.term.lastCommit') }}
            </th>
          </tr>
        </thead>
        <tbody>
          <BranchListItem
            v-for="branch in branches"
            :key="branch.branchId"
            :branch="branch"
          />
        </tbody>
      </table>
    </div>
  </div>
</template>

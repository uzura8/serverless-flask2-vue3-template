<script lang="ts">
import type { Server } from '@/types/Server'
import { defineComponent, ref, onBeforeMount } from 'vue'
import { storeToRefs } from 'pinia'
import { useUserStore } from '@/stores/user'
import { useGlobalLoaderStore } from '@/stores/globalLoader.js'
import { ServerApi } from '@/apis'
import ServerListItem from '@/components/molecules/ServerListItem.vue'

export default defineComponent({
  components: { ServerListItem },

  setup() {
    const globalLoader = useGlobalLoaderStore()

    const userStore = useUserStore()
    const { idToken } = storeToRefs(userStore)

    const servers = ref<Server[]>([])
    const setServers = async () => {
      try {
        globalLoader.updateLoading(true)
        const res = await ServerApi.getList(null, idToken.value)
        servers.value = res.items
        globalLoader.updateLoading(false)
      } catch (error) {
        console.error(error)
        globalLoader.updateLoading(false)
      }
    }

    onBeforeMount(async () => {
      await setServers()
    })

    return {
      servers
    }
  }
})
</script>

<template>
  <div>
    <p v-if="servers.length === 0">
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
              {{ $t('pgit.term.domain') }}
            </th>
            <th
              scope="col"
              class="px-4 py-3"
            >
              {{ $t('pgit.term.repositories') }}
            </th>
            <th
              scope="col"
              class="px-4 py-3"
            >
              {{ $t('common.lastUpdatedAt') }}
            </th>
          </tr>
        </thead>
        <tbody>
          <ServerListItem
            v-for="server in servers"
            :key="server.domain"
            :server="server"
          />
        </tbody>
      </table>
    </div>
  </div>
</template>

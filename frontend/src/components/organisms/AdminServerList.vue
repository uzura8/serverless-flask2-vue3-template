<script lang="ts">
import type { Server } from '@/types/Server'
import { defineComponent, ref, onBeforeMount } from 'vue'
import { useAdminUserStore } from '@/stores/adminUser'
import { useGlobalLoaderStore } from '@/stores/globalLoader.js'
import { AdminServerApi } from '@/apis'
import AdminServerListItem from '@/components/molecules/AdminServerListItem.vue'

export default defineComponent({
  components: { AdminServerListItem },

  setup() {
    const adminUser = useAdminUserStore()
    const globalLoader = useGlobalLoaderStore()

    const servers = ref<Server[]>([])
    const setServers = async () => {
      try {
        globalLoader.updateLoading(true)
        const res = await AdminServerApi.getList(null, adminUser.idToken)
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
              {{ $t('common.lastUpdatedAt') }}
            </th>
          </tr>
        </thead>
        <tbody>
          <AdminServerListItem
            v-for="server in servers"
            :key="server.domain"
            :server="server"
          />
        </tbody>
      </table>
    </div>
  </div>
</template>

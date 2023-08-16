<script lang="ts">
import type { Server } from '@/types/Server'
import { defineComponent, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useDate } from '@/composables/useDate'

export default defineComponent({
  components: {},

  props: {
    server: {
      type: Object as () => Server,
      required: true
    }
  },

  setup(props) {
    const { t } = useI18n()
    const { localeDate } = useDate()

    const statusLabel = computed(() => {
      if (props.server.isExecuting == '1') {
        return t('pgit.term.deployStatuses.inProgress')
      } else {
        return t('pgit.term.deployStatuses.completed')
      }
    })

    return {
      statusLabel,
      localeDate
    }
  }
})
</script>

<template>
  <tr class="border-b dark:border-gray-700">
    <td class="px-4 py-3">{{ statusLabel }}</td>
    <td class="px-4 py-3">{{ server.domain }}</td>
    <td class="px-4 py-3">
      <RouterLink
        :to="`/servers/${server.domain}/repositories`"
        class="text-blue-600 dark:text-blue-500 hover:underline"
      >
        {{ $t('common.list') }}
      </RouterLink>
    </td>
    <td class="px-4 py-3">
      <time
        itemprop="lastmodified"
        :datetime="localeDate(server.updatedAt)"
      >
        {{ localeDate(server.updatedAt, 'DATETIME_SHORT') }}
      </time>
    </td>
  </tr>
</template>

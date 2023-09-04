<script lang="ts">
import type { Branch } from '@/types/Branch'
import { defineComponent, computed } from 'vue'
import { useDate } from '@/composables/useDate'
import { sanitizeDomainStr } from '@/utils/str'
import config from '@/configs/config.json'
import PgDeployStatusUnit from '@/components/atoms/PgDeployStatusUnit.vue'

export default defineComponent({
  components: {
    PgDeployStatusUnit
  },

  props: {
    branch: {
      type: Object as () => Branch,
      required: true
    }
  },

  setup(props) {
    const { localeDate, formatDate } = useDate()

    const repoServices = computed(() => config.pgit.repository.services)
    const serviceLabel = computed(() => {
      const service = repoServices.value.find((s) => s.domain === props.branch.serviceDomain)
      return service ? service.label : ''
    })

    const branchBaseUrl = computed(() => {
      const items = [
        props.branch.serviceDomain,
        props.branch.serviceSegment,
        props.branch.repoName
      ].join('/')
      return `https://${items}`
    })

    const previewUrl = computed(() => {
      const items = [
        props.branch.repoCode,
        sanitizeDomainStr(props.branch.branchName),
        props.branch.serverDomain
      ].join('.')
      return `http://${items}`
    })

    return {
      serviceLabel,
      branchBaseUrl,
      previewUrl,
      localeDate,
      formatDate
    }
  }
})
</script>

<template>
  <tr class="border-b dark:border-gray-700">
    <td class="px-4 py-3">{{ branch.serverDomain }}</td>
    <td class="px-4 py-3">
      <span v-text="`${branch.serviceDomain}/${branch.serviceSegment}/${branch.repoName}`"> </span>
    </td>
    <td class="px-4 py-3">
      <a
        :href="`branchBaseUrl/tree/${branch.branchName}`"
        target="_blank"
        class="text-primary-600 dark:text-primary-500 hover:underline"
      >
        {{ branch.branchName }}
      </a>
      <FontAwesomeIcon
        icon="arrow-up-right-from-square"
        class="ml-2 text-gray-300"
      />
    </td>
    <td class="px-4 py-3">
      <a
        :href="previewUrl"
        target="_blank"
        class="text-xs text-primary-600 dark:text-primary-500 hover:underline"
      >
        {{ $t('common.doConfirm') }}
      </a>
      <FontAwesomeIcon
        icon="arrow-up-right-from-square"
        class="ml-2 text-gray-300"
      />
    </td>
    <td class="px-4 py-3 text-xs">
      <div>
        <a
          :href="`${branchBaseUrl}/commit/${branch.lastCommitInfo.hash}`"
          target="_blank"
          class="text-primary-600 dark:text-primary-500 hover:underline"
        >
          {{ branch.lastCommitInfo.hash }}
        </a>
      </div>
      <div>
        <span>{{ branch.lastCommitInfo.message }}</span>
      </div>
      <time
        class="text-sm"
        itemprop="lastmodified"
        :datetime="formatDate(branch.lastCommitInfo.date)"
      >
        {{ formatDate(branch.lastCommitInfo.date, 'yyyy/MM/dd HH:mm') }}
      </time>
    </td>
  </tr>
</template>

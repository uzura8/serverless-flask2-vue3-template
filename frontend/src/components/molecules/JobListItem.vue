<script lang="ts">
import type { Job } from '@/types/Job'
import { defineComponent, computed } from 'vue'
import { useDate } from '@/composables/useDate'
import config from '@/configs/config.json'
import PgDeployStatusUnit from '@/components/atoms/PgDeployStatusUnit.vue'

export default defineComponent({
  components: {
    PgDeployStatusUnit
  },

  props: {
    job: {
      type: Object as () => Job,
      required: true
    }
  },

  setup(props) {
    const { localeDate } = useDate()

    const repoServices = computed(() => config.pgit.repository.services)
    const serviceLabel = computed(() => {
      const service = repoServices.value.find((s) => s.domain === props.job.serviceDomain)
      return service ? service.label : ''
    })

    const repoUrl = computed(() => {
      const items = [props.job.serviceDomain, props.job.serviceSegment, props.job.repoName].join(
        '/'
      )
      return `https://${items}`
    })

    return {
      serviceLabel,
      repoUrl,
      localeDate
    }
  }
})
</script>

<template>
  <tr class="border-b dark:border-gray-700">
    <td class="px-4 py-3">
      <PgDeployStatusUnit :status="job.deployStatus" />
    </td>
    <td class="px-4 py-3">{{ job.serverDomain }}</td>
    <td class="px-4 py-3">
      <a
        :href="repoUrl"
        target="_blank"
        class="text-primary-600 dark:text-primary-500 hover:underline"
      >
        {{ serviceLabel }}
      </a>
      <FontAwesomeIcon
        icon="arrow-up-right-from-square"
        class="ml-2 text-gray-300"
      />
    </td>
    <td class="px-4 py-3">{{ job.serviceSegment }}</td>
    <td class="px-4 py-3">{{ job.repoName }}</td>
    <td class="px-4 py-3">{{ job.branchName }}</td>
    <td class="px-4 py-3">{{ job.deployType }}</td>
    <td class="px-4 py-3">
      <span v-if="job.isBuildRequired">{{ job.buildType }}</span>
      <span v-else>-</span>
    </td>
    <td class="px-4 py-3">
      <time
        itemprop="lastmodified"
        :datetime="localeDate(job.createdAt)"
      >
        {{ localeDate(job.createdAt, 'DATETIME_SHORT') }}
      </time>
    </td>
  </tr>
</template>

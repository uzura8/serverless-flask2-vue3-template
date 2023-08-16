<script lang="ts">
import type { Repository } from '@/types/Repository'
import { defineComponent, computed, onMounted } from 'vue'
import config from '@/configs/config.json'
import { initFlowbite } from 'flowbite'

export default defineComponent({
  components: {},

  props: {
    repo: {
      type: Object as () => Repository,
      required: true
    }
  },

  setup(props) {
    const repoServices = computed(() => config.pgit.repository.services)
    const serviceLabel = computed(() => {
      const service = repoServices.value.find((s) => s.domain === props.repo.serviceDomain)
      return service ? service.label : ''
    })

    const repoUrl = computed(() => {
      const items = [props.repo.serviceDomain, props.repo.serviceSegment, props.repo.repoName].join(
        '/'
      )
      return `https://${items}`
    })

    onMounted(async () => {
      initFlowbite()
    })

    return {
      serviceLabel,
      repoUrl
    }
  }
})
</script>

<template>
  <tr class="border-b dark:border-gray-700">
    <td class="px-4 py-3">{{ $t(`pgit.term.deployStatuses.${repo.deployStatus}`) }}</td>
    <td class="px-4 py-3">{{ repo.serverDomain }}</td>
    <td class="px-4 py-3">
      <a
        :href="repoUrl"
        target="_blank"
        class="text-blue-600 dark:text-blue-500 hover:underline"
      >
        {{ serviceLabel }}
      </a>
      <FontAwesomeIcon
        icon="arrow-up-right-from-square"
        class="ml-2 text-gray-300"
      />
    </td>
    <td class="px-4 py-3">{{ repo.serviceSegment }}</td>
    <td class="px-4 py-3">{{ repo.repoName }}</td>
    <td class="px-4 py-3">
      <span v-if="repo.isBuildRequired">{{ repo.buildType }}</span>
      <span v-else>-</span>
    </td>
    <td class="px-4 py-3 flex items-center justify-end">
      <button
        id="apple-imac-27-dropdown-button"
        data-dropdown-toggle="apple-imac-27-dropdown"
        class="inline-flex items-center p-0.5 text-sm font-medium text-center text-gray-500 hover:text-gray-800 rounded-lg focus:outline-none dark:text-gray-400 dark:hover:text-gray-100"
        type="button"
      >
        <FontAwesomeIcon
          icon="ellipsis"
          class="w-5 h-5"
        />
      </button>
      <div
        id="apple-imac-27-dropdown"
        class="hidden z-10 w-44 bg-white rounded divide-y divide-gray-100 shadow dark:bg-gray-700 dark:divide-gray-600"
      >
        <ul
          class="py-1 text-sm text-gray-700 dark:text-gray-200"
          aria-labelledby="apple-imac-27-dropdown-button"
        >
          <li>
            <a
              href="#"
              class="block py-2 px-4 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white"
              >Show</a
            >
          </li>
          <li>
            <a
              href="#"
              class="block py-2 px-4 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white"
              >Edit</a
            >
          </li>
        </ul>
        <div class="py-1">
          <a
            href="#"
            class="block py-2 px-4 text-sm text-gray-700 hover:bg-gray-100 dark:hover:bg-gray-600 dark:text-gray-200 dark:hover:text-white"
            >Delete</a
          >
        </div>
      </div>
    </td>
  </tr>
</template>

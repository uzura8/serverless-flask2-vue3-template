<script lang="ts">
import type { Job } from '@/types/Job'
import { defineComponent, ref, onBeforeMount } from 'vue'
import { storeToRefs } from 'pinia'
import { useUserStore } from '@/stores/user'
import { useGlobalLoaderStore } from '@/stores/globalLoader.js'
import { JobApi, ServerApi } from '@/apis'
import JobListItem from '@/components/molecules/JobListItem.vue'

export default defineComponent({
  components: { JobListItem },

  props: {
    serverDomain: {
      type: String as () => string | null,
      required: false
    }
  },

  setup(props) {
    const globalLoader = useGlobalLoaderStore()

    const userStore = useUserStore()
    const { idToken } = storeToRefs(userStore)

    const jobs = ref<Job[]>([])
    const setJobs = async () => {
      try {
        globalLoader.updateLoading(true)
        const params = { order: 'desc' }
        let res
        if (props.serverDomain) {
          res = await ServerApi.getJobs(props.serverDomain, params, idToken.value)
        } else {
          res = await JobApi.getList(params, idToken.value)
        }
        jobs.value = res.items
        globalLoader.updateLoading(false)
      } catch (error) {
        console.error(error)
        globalLoader.updateLoading(false)
      }
    }

    onBeforeMount(async () => {
      await setJobs()
    })

    return {
      jobs
    }
  }
})
</script>

<template>
  <div>
    <p v-if="jobs.length === 0">
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
              {{ $t('pgit.term.branch') }}
            </th>
            <th
              scope="col"
              class="px-4 py-3"
            >
              {{ $t('pgit.term.deployType') }}
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
              {{ $t('common.createdAt') }}
            </th>
          </tr>
        </thead>
        <tbody>
          <JobListItem
            v-for="job in jobs"
            :key="job.jobId"
            :job="job"
          />
        </tbody>
      </table>
    </div>
  </div>
</template>

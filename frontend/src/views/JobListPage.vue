<script lang="ts">
import { defineComponent } from 'vue'
import JobList from '@/components/organisms/JobList.vue'

export default defineComponent({
  components: {
    JobList
  },

  props: {},

  setup() {
    return {}
  }
})
</script>

<template>
  <h1 class="text-2xl font-semibold dark:text-white">{{ $t('pgit.term.jobList') }}</h1>
  <JobList class="mt-12" />
</template>

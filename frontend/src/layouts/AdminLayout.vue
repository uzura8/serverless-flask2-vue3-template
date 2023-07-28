<script lang="ts">
import { defineComponent } from 'vue'
import { storeToRefs } from 'pinia'
import { useGlobalLoaderStore } from '@/stores/globalLoader.js'
import LoadingSpinner from '@/components/molecules/LoadingSpinner.vue'
import AdminHeader from '@/components/organisms/AdminHeader.vue'
import MainFooter from '@/components/organisms/MainFooter.vue'

export default defineComponent({
  components: {
    LoadingSpinner,
    AdminHeader,
    MainFooter
  },

  setup() {
    // store
    const loader = useGlobalLoaderStore()
    const { isLoading: isGlobalLoading } = storeToRefs(loader)
    return { isGlobalLoading }
  }
})
</script>

<template>
  <div v-cloak>
    <LoadingSpinner
      v-if="isGlobalLoading"
      :is-fullscreen="true"
    />

    <div class="flex flex-col h-screen">
      <AdminHeader />

      <div class="flex-1">
        <div class="h-full max-w-[85rem] mx-auto">
          <main class="px-6 py-8">
            <RouterView />
          </main>
        </div>
      </div>

      <MainFooter />
    </div>
  </div>
</template>

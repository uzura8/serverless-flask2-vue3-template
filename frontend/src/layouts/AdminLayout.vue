<template>
  <div>
    <GlobalLoading v-if="isGlobalLoading" />

    <div class="flex flex-col h-screen">
      <AdminHeader />

      <div class="flex-1">
        <div class="h-full max-w-[85rem] mx-auto">
          <main class="px-6 py-10">
            <RouterView />
          </main>
        </div>
      </div>

      <MainFooter />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { storeToRefs } from 'pinia'
import { useGlobalLoaderStore } from '@/stores/globalLoader.js'
import GlobalLoading from '@/components/molecules/GlobalLoading.vue'
import AdminHeader from '@/components/organisms/AdminHeader.vue'
import MainFooter from '@/components/organisms/MainFooter.vue'

export default defineComponent({
  components: {
    GlobalLoading,
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

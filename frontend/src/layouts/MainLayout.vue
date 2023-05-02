<template>
  <div>
    <GlobalLoading v-if="isGlobalLoading" />

    <div class="flex flex-col h-screen">
      <MainHeader />

      <div class="flex-1">
        <div class="lg:grid lg:grid-cols-12 h-full max-w-[85rem] mx-auto">
          <main class="lg:col-span-9 lg:col-span-10 px-6 py-8">
            <RouterView />
          </main>

          <aside class="md:col-span-3 lg:col-span-2 p-6">Side</aside>
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
import MainHeader from '@/components/organisms/MainHeader.vue'
import MainFooter from '@/components/organisms/MainFooter.vue'

export default defineComponent({
  components: {
    GlobalLoading,
    MainHeader,
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

<script lang="ts">
import { defineComponent, ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import config from '@/configs/config.json'
import { useGlobalHeaderStore } from '@/stores/globalHeader'

export default defineComponent({
  components: {},

  setup() {
    const siteName = config.site.name

    const route = useRoute()
    const current = computed((): string => route.path)

    const header = ref<HTMLElement | null>(null)
    const globalHeader = useGlobalHeaderStore()
    const isMenuOpen = computed((): boolean => globalHeader.isMenuOpen)

    const toggleHeaderMenuOpenStatus = () => {
      globalHeader.updateMenuOpenStatus(!isMenuOpen.value)
    }

    const handleClickOutside = (event: MouseEvent) => {
      if (header.value && !header.value.contains(event.target as Node)) {
        globalHeader.updateMenuOpenStatus(false)
      }
    }

    onMounted(async () => {
      await nextTick(() => {
        header.value = document.querySelector('#header')
      })
      document.addEventListener('click', handleClickOutside)
    })

    onUnmounted(() => {
      document.removeEventListener('click', handleClickOutside)
    })

    return {
      current,
      siteName,
      isMenuOpen,
      toggleHeaderMenuOpenStatus
    }
  }
})
</script>

<template>
  <header
    id="header"
    class="flex flex-wrap sm:justify-start sm:flex-nowrap w-full bg-white text-sm py-5 xs:px-5 sm:px-7 dark:bg-gray-800 z-40"
  >
    <nav
      class="max-w-[85rem] w-full mx-auto sm:flex sm:items-center sm:justify-between"
      aria-label="Global"
    >
      <div class="flex items-center justify-between">
        <RouterLink
          to="/"
          class="flex-none text-3xl font-semibold dark:text-white"
        >
          {{ siteName }}
        </RouterLink>
        <div class="sm:hidden">
          <button
            @click="toggleHeaderMenuOpenStatus"
            type="button"
            :class="{ open: isMenuOpen }"
            class="hs-collapse-toggle p-2 inline-flex justify-center items-center gap-2 rounded-md border font-medium bg-white text-gray-700 shadow-sm align-middle hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-white focus:ring-blue-600 transition-all text-sm dark:bg-slate-900 dark:hover:bg-slate-800 dark:border-gray-700 dark:text-gray-400 dark:hover:text-white dark:focus:ring-offset-gray-800"
            data-hs-collapse="#navbar-with-collapse"
            aria-controls="navbar-with-collapse"
            aria-label="Toggle navigation"
          >
            <FontAwesomeIcon
              class="hs-collapse-open:hidden w-4 h-4"
              icon="bars"
            />
            <FontAwesomeIcon
              class="hs-collapse-open:block hidden w-4 h-4"
              icon="bars"
            />
          </button>
        </div>
      </div>
      <div
        :class="isMenuOpen ? 'open' : 'hidden'"
        id="navbar-with-collapse"
        class="basis-full grow sm:block"
      >
        <div class="flex flex-col gap-5 mt-5 sm:flex-row sm:items-center sm:mt-0 sm:pl-5">
          <RouterLink
            to="/"
            exact
            :aria-current="current === '/' ? 'page' : null"
            class="font-medium text-gray-600"
          >
            {{ $t('page.top') }}
          </RouterLink>
          <RouterLink
            to="/about"
            exact
            :aria-current="current === '/about' ? 'page' : null"
            class="font-medium text-gray-600"
          >
            {{ $t('page.about') }}
          </RouterLink>
          <RouterLink
            to="/posts"
            exact
            :aria-current="current === '/posts' ? 'page' : null"
            class="font-medium text-gray-600"
          >
            {{ $t('term.postList') }}
          </RouterLink>
        </div>
      </div>
    </nav>
  </header>
</template>

<style scoped>
.router-link-exact-active {
  color: #3b82f6;
}
</style>

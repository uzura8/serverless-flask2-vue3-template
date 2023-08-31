<script lang="ts">
import { defineComponent, ref, computed, watch, onMounted, onUnmounted, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import config from '@/configs/config.json'
import { storeToRefs } from 'pinia'
import { useGlobalHeaderStore } from '@/stores/globalHeader'
import { useGlobalLoaderStore } from '@/stores/globalLoader'
import { FirebaseApi } from '@/apis'
import { useUserStore } from '@/stores/user'

export default defineComponent({
  components: {},

  setup() {
    const siteName = config.site.name

    const router = useRouter()
    const route = useRoute()
    const current = computed((): string => route.path)

    const globalLoader = useGlobalLoaderStore()

    const userStore = useUserStore()
    const { isAuth } = storeToRefs(userStore)

    const signOut = async () => {
      try {
        globalLoader.updateLoading(true)
        await FirebaseApi.signOut()
        userStore.setUser(null)
        globalLoader.updateLoading(false)
        router.push('/signin')
      } catch (error) {
        console.error(error)
        globalLoader.updateLoading(false)
      }
    }

    const header = ref<HTMLElement | null>(null)
    const globalHeader = useGlobalHeaderStore()
    const isMenuOpen = computed((): boolean => globalHeader.isMenuOpen)

    // Calculate the height of the menu and set it to the animation
    const setAnimationHeight = (): void => {
      const navbar = document.getElementById('navbar-with-collapse')
      if (!navbar) return

      if (isMenuOpen.value) {
        navbar.style.maxHeight = '0'
        navbar.classList.remove('hidden')
        navbar.classList.add('open')
        navbar.style.maxHeight = `${navbar.scrollHeight}px`
      } else {
        navbar.style.maxHeight = '0'
        navbar.classList.remove('open')
        setTimeout(() => {
          navbar.classList.add('hidden')
          navbar.style.maxHeight = ''
        }, 300)
      }
    }

    watch(isMenuOpen, () => {
      setAnimationHeight()
    })

    const toggleHeaderMenuOpenStatus = () => {
      globalHeader.updateMenuOpenStatus(!isMenuOpen.value)
    }

    const handleClickOutside = (event: MouseEvent) => {
      if (header.value && !header.value.contains(event.target as Node)) {
        globalHeader.updateMenuOpenStatus(false)
      }
    }

    onMounted(async () => {
      nextTick(() => {
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
      isAuth,
      signOut,
      isMenuOpen,
      toggleHeaderMenuOpenStatus
    }
  }
})
</script>

<style scoped>
.router-link-exact-active {
  color: #3b82f6;
}
</style>

<template>
  <header
    id="header"
    class="flex flex-wrap sm:justify-start sm:flex-nowrap w-full bg-white text-sm py-2 xs:px-5 dark:bg-gray-800 z-40"
  >
    <nav
      class="max-w-[85rem] w-full mx-auto px-4 sm:flex sm:items-center sm:justify-between"
      aria-label="Global"
    >
      <div class="flex items-center justify-between">
        <RouterLink
          to="/"
          class="flex-none text-xl font-medium dark:text-white py-1"
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
        id="navbar-with-collapse"
        class="hs-collapse hidden overflow-hidden transition-all ease-in-out duration-300 basis-full grow sm:block md:ml-10"
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
            v-if="isAuth"
            to="/servers"
            exact
            :aria-current="current === '/servers' ? 'page' : null"
            class="font-medium text-gray-600"
            :class="{ 'router-link-exact-active': current.startsWith('/servers') }"
          >
            {{ $t('pgit.term.servers') }}
          </RouterLink>
          <RouterLink
            v-if="isAuth"
            to="/repositories"
            exact
            :aria-current="current === '/repositories' ? 'page' : null"
            class="font-medium text-gray-600"
            :class="{ 'router-link-exact-active': current.startsWith('/repositories') }"
          >
            {{ $t('pgit.term.repositories') }}
          </RouterLink>
          <RouterLink
            v-if="isAuth"
            to="/jobs"
            exact
            :aria-current="current === '/jobs' ? 'page' : null"
            class="font-medium text-gray-600"
            :class="{ 'router-link-exact-active': current.startsWith('/jobs') }"
          >
            {{ $t('pgit.term.jobs') }}
          </RouterLink>
          <RouterLink
            v-if="!isAuth"
            to="/signin"
            exact
            :aria-current="current === '/signin' ? 'page' : null"
            class="font-medium text-gray-600"
          >
            {{ $t('common.signIn') }}
          </RouterLink>
          <RouterLink
            v-if="isAuth"
            to="/member"
            exact
            :aria-current="current === '/member' ? 'page' : null"
            class="font-medium text-gray-600"
          >
            {{ $t('page.userTop') }}
          </RouterLink>
          <a
            v-if="isAuth"
            @click="signOut"
            class="font-medium text-gray-600 cursor-pointer"
          >
            {{ $t('common.signOut') }}
          </a>
        </div>
      </div>
    </nav>
  </header>
</template>

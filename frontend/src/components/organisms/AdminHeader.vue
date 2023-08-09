<script lang="ts">
import { defineComponent, ref, computed, watch, onMounted, onUnmounted, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import config from '@/configs/config.json'
//import { storeToRefs } from 'pinia'
import { useGlobalHeaderStore } from '@/stores/globalHeader'
import { useGlobalLoaderStore } from '@/stores/globalLoader'
import { AdminAuthApi } from '@/apis'
import { useAdminUserStore } from '@/stores/adminUser'
import AdminHeaderUserDropdown from '@/components/molecules/AdminHeaderUserDropdown.vue'

export default defineComponent({
  components: {
    AdminHeaderUserDropdown
  },

  setup() {
    const siteName = config.site.name

    const router = useRouter()
    const route = useRoute()
    const current = computed((): string => route.path)

    const globalLoader = useGlobalLoaderStore()

    const adminUser = useAdminUserStore()
    const isAuth = computed((): boolean => adminUser.isAuthenticated)
    const username = computed((): string => {
      if (!adminUser.isAuthenticated) return ''
      return adminUser.username ?? ''
    })

    const signOut = async () => {
      try {
        globalLoader.updateLoading(true)
        await AdminAuthApi.signOut()
        adminUser.setUser(null)
        globalLoader.updateLoading(false)
        router.push('/admin/signin')
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
      username,
      signOut,
      isMenuOpen,
      toggleHeaderMenuOpenStatus
    }
  }
})
</script>

<style scoped></style>

<template>
  <header id="header">
    <nav class="bg-white border-gray-200 px-4 lg:px-6 py-2.5 dark:bg-gray-800">
      <div class="flex flex-wrap justify-between items-center mx-auto max-w-screen-xl">
        <RouterLink
          to="/admin"
          class="flex items-center"
        >
          <span class="self-center text-xl font-semibold whitespace-nowrap dark:text-white">
            {{ siteName }}
          </span>
        </RouterLink>
        <div class="flex items-center lg:order-2">
          <AdminHeaderUserDropdown
            v-if="isAuth"
            :username="username"
            @sign-out="signOut"
          />
          <RouterLink
            v-else
            to="/admin/signin"
            class="text-gray-900 hover:text-white border border-gray-800 hover:bg-gray-900 focus:ring-4 focus:outline-none focus:ring-gvay-300 font-medium rounded-lg text-sm px-4 lg:px-5 py-2 lg:py-2.5 mr-2 text-center dark:border-gray-600 dark:text-gray-400 dark:hover:text-white dark:hover:bg-gray-600 dark:focus:ring-gray-800"
          >
            {{ $t('common.signIn') }}
          </RouterLink>
          <button
            @click="toggleHeaderMenuOpenStatus"
            type="button"
            :class="{ open: isMenuOpen }"
            class="inline-flex items-center p-2 ml-1 text-sm text-gray-500 rounded-lg lg:hidden hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-200 dark:text-gray-400 dark:hover:bg-gray-700 dark:focus:ring-gray-600"
          >
            <span class="sr-only">Open main menu</span>
            <FontAwesomeIcon
              class="hs-collapse-open:hidden w-6 h-6"
              icon="bars"
            />
            <FontAwesomeIcon
              class="hs-collapse-open:block hidden w-6 h-6"
              icon="bars"
            />
          </button>
        </div>
        <div
          id="navbar-with-collapse"
          class="hidden overflow-hidden transition-all ease-in-out duration-300 justify-between items-center w-full lg:flex lg:w-auto lg:order-1"
        >
          <ul class="flex flex-col mt-4 font-medium lg:flex-row lg:space-x-8 lg:mt-0">
            <li>
              <RouterLink
                to="/admin"
                class="block py-4 pr-4 pl-3 text-gray-700 border-b border-gray-100 hover:bg-gray-50 lg:hover:bg-transparent lg:border-0 lg:hover:text-primary-700 lg:p-0 dark:text-gray-400 lg:dark:hover:text-white dark:hover:bg-gray-700 dark:hover:text-white lg:dark:hover:bg-transparent dark:border-gray-700"
                exact-active-class="bg-transparent text-primary-700"
              >
                Top
              </RouterLink>
            </li>
            <li>
              <RouterLink
                to="/admin/about"
                class="block py-4 pr-4 pl-3 text-gray-700 border-b border-gray-100 hover:bg-gray-50 lg:hover:bg-transparent lg:border-0 lg:hover:text-primary-700 lg:p-0 dark:text-gray-400 lg:dark:hover:text-white dark:hover:bg-gray-700 dark:hover:text-white lg:dark:hover:bg-transparent dark:border-gray-700"
                exact-active-class="bg-transparent text-primary-700"
              >
                {{ $t('page.about') }}
              </RouterLink>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </header>
</template>

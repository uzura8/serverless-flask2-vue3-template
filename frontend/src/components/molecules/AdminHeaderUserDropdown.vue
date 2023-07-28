<script lang="ts">
import { defineComponent, onMounted } from 'vue'
import { initFlowbite } from 'flowbite'

export default defineComponent({
  components: {},

  props: {
    username: {
      type: String,
      required: true
    }
  },

  setup(_, context) {
    const signOut = async () => {
      context.emit('sign-out')
    }

    onMounted(async () => {
      initFlowbite()
    })

    return {
      signOut
    }
  }
})
</script>

<template>
  <button
    type="button"
    id="user-menu-button"
    aria-expanded="false"
    data-dropdown-toggle="user-dropdown"
    data-dropdown-placement="bottom"
    class="flex text-gray-500 bg-white border border-gray-300 focus:outline-none hover:bg-gray-100 focus:ring-4 focus:ring-gray-200 font-medium rounded-lg text-md px-3 py-2.5 mr-2 mb-2 mt-2 leading-4 dark:bg-gray-800 dark:text-white dark:border-gray-600 dark:hover:bg-gray-700 dark:hover:border-gray-600 dark:focus:ring-gray-700"
  >
    <FontAwesomeIcon
      class="w-6 h-6 mr-2"
      icon="circle-user"
    />
    <span class="pt-1">{{ username }}</span>
  </button>
  <!-- Dropdown menu -->
  <div
    class="hidden min-w-150 z-50 my-1 text-base list-none bg-white divide-y divide-gray-100 rounded-lg shadow dark:bg-gray-700 dark:divide-gray-600"
    id="user-dropdown"
  >
    <div class="px-4 py-3">
      <span class="block text-sm text-gray-900 dark:text-white">{{ username }}</span>
    </div>
    <ul
      class="py-2"
      aria-labelledby="user-menu-button"
    >
      <li>
        <a
          href="#"
          class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 dark:hover:bg-gray-600 dark:text-gray-200 dark:hover:text-white"
        >
          {{ $t('page.settings') }}
        </a>
      </li>
      <li>
        <button
          type="button"
          class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 dark:hover:bg-gray-600 dark:text-gray-200 dark:hover:text-white"
          @click="signOut"
        >
          {{ $t('common.signOut') }}
        </button>
      </li>
    </ul>
  </div>
</template>

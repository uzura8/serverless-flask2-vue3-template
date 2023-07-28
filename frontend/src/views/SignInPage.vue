<script lang="ts">
import { defineComponent } from 'vue'
import SignInForm from '@/components/organisms/SignInForm.vue'

export default defineComponent({
  components: {
    SignInForm
  },

  setup() {}
})
</script>

<template>
  <div class="flex flex-col items-center justify-center px-0 py-8 mx-auto">
    <div
      class="w-full bg-white rounded-lg shadow dark:border md:mt-0 sm:max-w-md xl:p-0 dark:bg-gray-800 dark:border-gray-700"
    >
      <div class="p-6 space-y-4 sm:p-8">
        <h1
          class="mb-10 text-xl font-bold leading-tight tracking-tight text-gray-900 dark:text-white"
        >
          {{ $t('common.signIn') }}
        </h1>
        <SignInForm />
      </div>
    </div>
  </div>
</template>

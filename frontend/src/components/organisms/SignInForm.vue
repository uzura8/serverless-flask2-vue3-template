<script lang="ts">
import { defineComponent, ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { checkEmail } from '@/utils/str'
import { useGlobalLoaderStore } from '@/stores/globalLoader'
import { useAdminUserStore } from '@/stores/adminUser'
import { useUserStore } from '@/stores/user'
import { AdminAuthApi, FirebaseApi } from '@/apis'

interface FieldErrors {
  email: string
  password: string
}

export default defineComponent({
  props: {
    isAdmin: {
      type: Boolean,
      default: false
    }
  },

  setup(props) {
    const router = useRouter()
    const { t } = useI18n()
    const globalLoader = useGlobalLoaderStore()

    const errors = ref<FieldErrors>({ email: '', password: '' })
    const hasErrors = computed(() => {
      return Object.values(errors.value).some((error) => error)
    })

    const email = ref<string>('')
    const validateEmail = () => {
      errors.value.email = ''
      if (!email.value) {
        errors.value.email = t('msg.inputRequired')
      } else if (!checkEmail(email.value)) {
        errors.value.email = t('msg.inputInvalid')
      }
    }

    const password = ref<string>('')
    const showPassword = ref<boolean>(false)
    const validatePassword = () => {
      errors.value.password = ''
      if (!password.value) {
        errors.value.password = t('msg.inputRequired')
      } else if (password.value.length < 6) {
        errors.value.password = t('msg.atLeastCharacters', { count: 6 })
      }
    }

    const validateAll = () => {
      validateEmail()
      validatePassword()
    }

    const signInFirebase = async () => {
      const userStore = useUserStore()
      globalLoader.updateLoading(true)
      try {
        const userCredential = await FirebaseApi.signIn(email.value, password.value)
        userStore.setUser(userCredential.user)
        globalLoader.updateLoading(false)
        router.push('/home')
      } catch (error) {
        console.error(error)
        globalLoader.updateLoading(false)
      }
    }

    const signInCognito = async () => {
      const adminUser = useAdminUserStore()
      globalLoader.updateLoading(true)
      try {
        const user = await AdminAuthApi.signIn(email.value, password.value)
        if (!user) throw new Error('Failed to sign in')
        adminUser.setUser(user)
        globalLoader.updateLoading(false)
        router.push('/admin')
      } catch (error) {
        console.error(error)
        globalLoader.updateLoading(false)
      }
    }

    const signIn = async () => {
      validateAll()
      if (hasErrors.value) return

      if (props.isAdmin) {
        await signInCognito()
      } else {
        await signInFirebase()
      }
    }

    return {
      errors,
      hasErrors,
      email,
      validateEmail,
      password,
      showPassword,
      validatePassword,
      signIn
    }
  }
})
</script>

<template>
  <form class="space-y-10">
    <div>
      <label
        for="email"
        class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
      >
        {{ $t('common.email') }}
      </label>
      <input
        v-model="email"
        @blur="validateEmail"
        type="email"
        class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
        :class="{ 'border-red-700': errors.email }"
        placeholder="name@example.com"
      />
      <p
        v-if="errors.email"
        class="mt-2 text-sm text-red-700 dark:text-red-700"
      >
        {{ errors.email }}
      </p>
    </div>
    <div>
      <label
        for="password"
        class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
      >
        {{ $t('common.password') }}
      </label>
      <div class="relative">
        <input
          v-model="password"
          @blur="validatePassword"
          :type="showPassword ? 'text' : 'password'"
          class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
          :class="{ 'border-red-700': errors.password }"
        />
        <a
          @click="showPassword = !showPassword"
          class="absolute inset-y-0 right-0 flex items-center cursor-pointer pr-3 text-primary-600"
        >
          <FontAwesomeIcon
            v-if="!showPassword"
            class="w-5 h-5"
            icon="eye"
          />
          <FontAwesomeIcon
            v-else
            class="w-5 h-5"
            icon="eye-slash"
          />
        </a>
      </div>
      <p
        v-if="errors.password"
        class="mt-2 text-sm text-red-600 dark:text-red-400"
      >
        {{ errors.password }}
      </p>
    </div>
    <button
      @click="signIn"
      :disabled="hasErrors"
      type="button"
      class="w-full text-white bg-primary-600 hover:bg-primary-700 focus:ring-4 focus:outline-none focus:ring-primary-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-primary-600 dark:hover:bg-primary-700 dark:focus:ring-primary-800 disabled:opacity-50 disabled:cursor-not-allowed"
    >
      {{ $t('common.signIn') }}
    </button>
  </form>
</template>

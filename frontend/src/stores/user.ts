import type { User } from '@firebase/auth'
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', () => {
  // state
  const user = ref<User | null>(null)
  const idToken = ref<string | null>(null)

  const isAuth = computed((): boolean => {
    return user.value !== null
  })

  // mutations
  const setUser = (authedUser: User | null): void => {
    user.value = authedUser ? authedUser : null
  }

  const setIdToken = (token: string | null): void => {
    idToken.value = token
  }

  return {
    user,
    idToken,
    isAuth,
    setUser,
    setIdToken
  }
})

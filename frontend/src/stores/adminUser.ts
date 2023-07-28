import type { CognitoUser, CognitoUserSession } from 'amazon-cognito-identity-js'
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useAdminUserStore = defineStore('adminUser', () => {
  // state
  const adminUser = ref<CognitoUser | null>(null)

  // getters
  const session = computed((): CognitoUserSession | null => {
    if (!adminUser.value) return null
    return adminUser.value.getSignInUserSession()
  })

  const username = computed((): string | null => {
    if (!adminUser.value) return null
    return adminUser.value.getUsername()
  })

  const isAuthenticated = computed((): boolean => {
    return !!session.value
  })

  // mutations
  const setUser = (user: CognitoUser | null): void => {
    adminUser.value = user
  }

  return {
    adminUser,
    session,
    isAuthenticated,
    username,
    setUser
  }
})

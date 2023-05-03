import type { CognitoUser, CognitoUserSession } from 'amazon-cognito-identity-js'
import '@/amplify-config'
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { Auth } from 'aws-amplify'

export const useAdminUserStore = defineStore('adminUser', () => {
  // state
  const adminUser = ref<CognitoUser | null>(null)

  // getters
  const session = computed((): CognitoUserSession | null => {
    if (!adminUser.value) return null
    return adminUser.value.getSignInUserSession()
  })

  const isAuthenticated = computed((): boolean => {
    return !!session.value
  })

  // mutations
  const setUser = (user: CognitoUser | null): void => {
    adminUser.value = user
  }

  const checkAndSetCurrentUser = async (): Promise<boolean> => {
    const currentUser = await Auth.currentAuthenticatedUser()
    if (!currentUser) return false

    setUser(currentUser)
    return true
  }

  const signIn = async (email: string, password: string): Promise<CognitoUser | null> => {
    const user = await Auth.signIn(email, password)
    if (!user) return null

    setUser(user)
    return user
  }

  return {
    adminUser,
    session,
    isAuthenticated,
    setUser,
    checkAndSetCurrentUser,
    signIn
  }
})

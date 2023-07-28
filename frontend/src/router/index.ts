import type { RouterScrollBehavior } from 'vue-router'
import { createRouter, createWebHistory } from 'vue-router'
import { AdminAuthApi, FirebaseApi } from '@/apis'
import { useGlobalHeaderStore } from '@/stores/globalHeader'
import { useGlobalLoaderStore } from '@/stores/globalLoader'
import { useAdminUserStore } from '@/stores/adminUser'
import { useUserStore } from '@/stores/user'
import routes from './routes'

const scrollBehavior: RouterScrollBehavior = (to, _from, savedPosition) => {
  if (to.hash) {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          el: to.hash
          //behavior: 'smooth'
        })
      }, 500)
    })
  } else if (savedPosition) {
    return new Promise((resolve) => {
      setTimeout(() => {
        //savedPosition.behavior = 'smooth'
        resolve(savedPosition)
      }, 500)
    })
  } else {
    return { left: 0, top: 0 }
  }
}

const router = createRouter({
  routes,
  history: createWebHistory(import.meta.env.BASE_URL),
  scrollBehavior
})

router.beforeEach(async (to, _from, next) => {
  const globalHeader = useGlobalHeaderStore()
  globalHeader.updateMenuOpenStatus(false)
  const globalLoader = useGlobalLoaderStore()

  const isAdminPath = to.path.startsWith('/admin')
  const requiresAuth = to.matched.some((record) => record.meta.requiresAuth)
  let user = null
  let authForcedRedirectPaths = []

  if (isAdminPath) {
    // Admin User Auth
    authForcedRedirectPaths = [
      '/admin/signin',
      '/admin/signup',
      '/admin/forgot-password',
      '/admin/reset-password'
    ]
    const adminUser = useAdminUserStore()
    try {
      globalLoader.updateLoading(true)
      user = await AdminAuthApi.currentAuthenticatedUser()
      globalLoader.updateLoading(false)
    } catch (error) {
      //console.error(error)
      globalLoader.updateLoading(false)
    }
    adminUser.setUser(user)
  } else {
    // User Auth
    authForcedRedirectPaths = ['/signin', '/signup', '/forgot-password', '/reset-password']
    const userStore = useUserStore()
    user = FirebaseApi.getCurrentUser()
    if (!user) {
      user = await FirebaseApi.onAuthStateChanged()
    }
    userStore.setUser(user)
    if (user) {
      const idToken = await user.getIdToken()
      userStore.setIdToken(idToken)
    }
  }

  if (user) {
    if (authForcedRedirectPaths.includes(to.path)) {
      next({ path: isAdminPath ? '/admin' : '/home' })
      return
    }
  } else {
    if (requiresAuth) {
      next({ path: isAdminPath ? '/admin/signin' : '/signin' })
      return
    }
  }
  next()
})

export default router

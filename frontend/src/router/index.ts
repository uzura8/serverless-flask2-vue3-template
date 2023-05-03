import { createRouter, createWebHistory } from 'vue-router'
import { useGlobalHeaderStore } from '@/stores/globalHeader'
import { useGlobalLoaderStore } from '@/stores/globalLoader'
import { useAdminUserStore } from '@/stores/adminUser'
import { AdminAuthApi } from '@/apis'
import routes from './routes'

const router = createRouter({
  routes,
  history: createWebHistory(import.meta.env.BASE_URL)
})

router.beforeEach(async (to, _from, next) => {
  const globalHeader = useGlobalHeaderStore()
  const globalLoader = useGlobalLoaderStore()
  const adminUser = useAdminUserStore()

  globalHeader.updateMenuOpenStatus(false)

  const authForcedRedirectPaths = [
    '/admin/sign-in',
    '/admin/sign-up',
    '/admin/forgot-password',
    '/admin/reset-password'
  ]

  let user = null
  try {
    globalLoader.updateLoading(true)
    user = await AdminAuthApi.currentAuthenticatedUser()
    globalLoader.updateLoading(false)
  } catch (error) {
    //console.error(error)
    globalLoader.updateLoading(false)
  }
  adminUser.setUser(user)

  const requiredAuth = to.matched.some((record) => record.meta.requiresAuth)

  if (user) {
    if (authForcedRedirectPaths.includes(to.path)) {
      next({ path: '/admin' })
      return
    }
  } else {
    if (requiredAuth) {
      next({ path: '/admin/sign-in' })
      return
    }
  }
  next()
})

export default router

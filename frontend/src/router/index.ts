import { createRouter, createWebHistory } from 'vue-router'
import { useGlobalHeaderStore } from '@/stores/globalHeader'
import routes from './routes'

const router = createRouter({
  routes,
  history: createWebHistory(import.meta.env.BASE_URL)
})

router.beforeEach(() => {
  const globalHeader = useGlobalHeaderStore()
  globalHeader.updateMenuOpenStatus(false)
})

export default router

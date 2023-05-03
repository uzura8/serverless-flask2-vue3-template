import type { RouteRecordRaw } from 'vue-router'
import MainLayout from '@/layouts/MainLayout.vue'
import AdminLayout from '@/layouts/AdminLayout.vue'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: MainLayout,
    children: [
      {
        path: '',
        name: 'TopPage',
        component: () => import('@/views/TopPage.vue')
      },
      {
        path: 'about',
        name: 'AboutPage',
        component: () => import('@/views/AboutPage.vue')
      },
      {
        path: 'posts',
        name: 'PostListPage',
        component: () => import('@/views/PostListPage.vue')
      },
      {
        path: 'posts/:slug',
        name: 'PostDetailPage',
        component: () => import('@/views/PostDetailPage.vue')
      }
    ]
  },
  {
    path: '/admin',
    component: AdminLayout,
    children: [
      {
        path: '',
        name: 'AdminTopPage',
        component: () => import('@/views/AdminTopPage.vue')
      },
      {
        path: 'sign-in',
        name: 'AdminSignInPage',
        component: () => import('@/views/AdminSignInPage.vue')
      }
    ]
  },
  {
    path: '/:catchAll(.*)*',
    component: () => import('@/views/NotFound.vue')
  }
]

export default routes

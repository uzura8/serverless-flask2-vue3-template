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
        path: '/home',
        name: 'HomePage',
        component: () => import('@/views/HomePage.vue'),
        meta: {
          requiresAuth: true
        }
      },
      {
        path: '/signin',
        name: 'SignInPage',
        component: () => import('@/views/SignInPage.vue')
      },
      {
        path: '/about',
        name: 'AboutPage',
        component: () => import('@/views/AboutPage.vue')
      },
      {
        path: '/posts',
        name: 'PostListPage',
        component: () => import('@/views/PostListPage.vue')
      },
      {
        path: '/posts/:slug',
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
        path: '/admin',
        name: 'AdminTopPage',
        component: () => import('@/views/AdminTopPage.vue'),
        meta: {
          requiresAuth: true
        }
      },
      {
        path: '/admin/signin',
        name: 'AdminSignIn',
        component: () => import('@/views/AdminSignInPage.vue')
      },
      {
        path: '/admin/about',
        name: 'AdminAboutPage',
        component: () => import('@/views/AdminAboutPage.vue'),
        meta: {
          requiresAuth: true
        }
      },
      {
        path: '/admin/repositories',
        name: 'AdminRepoListPage',
        component: () => import('@/views/AdminRepoListPage.vue'),
        meta: {
          requiresAuth: true
        }
      },
      {
        path: '/admin/repositories/create',
        name: 'AdminRepoCreatePage',
        component: () => import('@/views/AdminRepoCreatePage.vue'),
        meta: {
          requiresAuth: true
        }
      }
    ]
  },
  {
    path: '/:catchAll(.*)*',
    component: () => import('@/views/NotFound.vue')
  }
]

export default routes

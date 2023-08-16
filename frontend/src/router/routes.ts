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
        path: '/servers',
        name: 'ServerListPage',
        component: () => import('@/views/ServerListPage.vue'),
        meta: {
          requiresAuth: true
        }
      },
      {
        path: '/repositories',
        name: 'RepoListPage',
        component: () => import('@/views/RepoListPage.vue'),
        meta: {
          requiresAuth: true
        }
      },
      {
        path: '/repositories/create',
        name: 'RepoCreatePage',
        component: () => import('@/views/RepoCreatePage.vue'),
        meta: {
          requiresAuth: true
        }
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
      }
    ]
  },
  {
    path: '/:catchAll(.*)*',
    component: () => import('@/views/NotFound.vue')
  }
]

export default routes

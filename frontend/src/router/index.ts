import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import { useUserStore } from '@/stores/user'

const routes: RouteRecordRaw[] = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/',
    redirect: '/users',
    component: () => import('@/views/Layout.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: 'users',
        name: 'Users',
        component: () => import('@/views/Users.vue'),
        meta: { requiresAuth: true }
      },
      {
        path: 'configs',
        name: 'Configs',
        component: () => import('@/views/Configs.vue'),
        meta: { requiresAuth: true }
      },
      {
        path: 'nodes',
        name: 'Nodes',
        component: () => import('@/views/Nodes.vue'),
        meta: { requiresAuth: true }
      },
      {
        path: 'testcases',
        name: 'TestCases',
        component: () => import('@/views/TestCases.vue'),
        meta: { requiresAuth: true }
      },
      {
        path: 'jmxs',
        name: 'Jmxs',
        component: () => import('@/views/Jmxs.vue'),
        meta: { requiresAuth: true }
      },
      {
        path: 'jars',
        name: 'Jars',
        component: () => import('@/views/Jars.vue'),
        meta: { requiresAuth: true }
      },
      {
        path: 'csvs',
        name: 'Csvs',
        component: () => import('@/views/Csvs.vue'),
        meta: { requiresAuth: true }
      },
      {
        path: 'reports',
        name: 'Reports',
        component: () => import('@/views/Reports.vue'),
        meta: { requiresAuth: true }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach(async (to, from, next) => {
  const userStore = useUserStore()
  const requiresAuth = to.meta.requiresAuth !== false

  if (requiresAuth && !userStore.token) {
    next('/login')
  } else if (to.path === '/login' && userStore.token) {
    next('/')
  } else {
    if (requiresAuth && !userStore.user) {
      try {
        await userStore.fetchUser()
      } catch (error) {
        next('/login')
        return
      }
    }
    next()
  }
})

export default router


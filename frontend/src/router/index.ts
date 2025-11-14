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

  console.log('路由守卫：', {
    to: to.path,
    hasToken: !!userStore.token,
    hasUser: !!userStore.user,
    requiresAuth
  })

  // 如果去登录页且已有token，直接跳转到首页
  if (to.path === '/login' && userStore.token) {
    console.log('已登录，跳转到首页')
    next('/users')
    return
  }

  // 如果需要认证但没有token，跳转到登录页
  if (requiresAuth && !userStore.token) {
    console.log('未登录，跳转到登录页')
    next('/login')
    return
  }

  // 如果需要认证且有token但没有用户信息，获取用户信息
  if (requiresAuth && userStore.token && !userStore.user) {
    console.log('有token但无用户信息，尝试获取用户信息')
    try {
      await userStore.fetchUser()
      console.log('用户信息获取成功')
      next()
    } catch (error) {
      console.error('获取用户信息失败，清除token并跳转到登录页')
      userStore.clearAuth()
      next('/login')
    }
    return
  }

  // 其他情况直接通过
  next()
})

export default router


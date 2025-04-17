import { createRouter, createWebHashHistory } from 'vue-router'
import Login from '@/components/Login.vue';
import Register from '@/components/Register.vue';

const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/HomeView.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
      path: '/Register',
      name: 'Register',
      component: Register
    },
    // {
    //   path: '/about',
    //   name: 'about',
    //   component: () => import('../views/AboutView.vue')
    // }
  ]
})

// 全局导航守卫
router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('userToken'); // 检查用户是否有登录标识

  if (to.matched.some((record) => record.meta.requiresAuth)) {
    // 如果路由需要认证
    if (!isAuthenticated) {
      // 未认证，重定向到登录页面
      next({ path: '/login' });
    } else {
      // 已登录，允许访问
      next();
    }
  } else {
    // 不需要登录的页面，允许访问
    next();
  }
});

export default router;

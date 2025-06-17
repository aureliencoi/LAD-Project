import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import { useAuthStore } from '@/stores/auth.store'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/home',
      name: 'home',
      component: () => import('../views/HomeView.vue')
    },
    // --- NOUVELLES ROUTES DE DÉTAIL ---
    {
      path: '/movie/:id',
      name: 'movie-detail',
      component: () => import('../views/MediaDetailView.vue')
    },
    {
      path: '/series/:id',
      name: 'series-detail',
      component: () => import('../views/MediaDetailView.vue')
    },
    // --- FIN DES NOUVELLES ROUTES ---
    {
      path: '/',
      redirect: '/home'
    }
  ]
})

router.beforeEach(async (to) => {
  const authStore = useAuthStore();
  const publicPages = ['/login'];
  const authRequired = !publicPages.includes(to.path);

  if (authRequired && !authStore.isLoggedIn) {
    return '/login';
  }
});

export default router
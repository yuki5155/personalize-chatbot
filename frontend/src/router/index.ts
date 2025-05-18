import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router';
import store from '../store';

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/HomePage.vue')
  },
  {
    path: '/chat',
    name: 'Chat',
    component: () => import('../views/ChatPage.vue'),
    meta: {
      requiresAuth: true
    }
  },
  {
    path: '/mypage',
    name: 'MyPage',
    component: () => import('../views/MyPage.vue'),
    meta: {
      requiresAuth: true
    }
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

// ナビゲーションガード
router.beforeEach((to, from, next) => {
  // 認証が必要なルートかチェック
  if (to.matched.some(record => record.meta.requiresAuth)) {
    // 認証状態をチェック
    if (!store.getters['auth/isAuthenticated']) {
      // 認証されていない場合はホームページにリダイレクト
      next({ path: '/' });
    } else {
      // 認証されている場合は続行
      next();
    }
  } else {
    // 認証が必要ないルートは制限なく続行
    next();
  }
});

export default router; 
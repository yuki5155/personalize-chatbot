import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router';
import store from '../store';
import { userService } from '../api/services';

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
router.beforeEach(async (to, from, next) => {
  // 認証状態を毎回APIから取得
  try {
    await store.dispatch('auth/checkAuth');
  } catch (error) {
    console.error('認証状態の確認中にエラーが発生しました:', error);
  }

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
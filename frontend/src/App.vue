<template>
  <div class="app-container">
    <header>
      <nav>
        <div class="nav-links">
          <router-link to="/">Home</router-link>
          <template v-if="isAuthenticated">
            | <router-link to="/chat">Chat</router-link> |
            <router-link to="/mypage">MyPage</router-link>
          </template>
        </div>
        
        <div class="auth-buttons">
          <template v-if="isAuthenticated">
            <span class="welcome-text">ようこそ、{{ getUserName() }}さん</span>
            <button @click="logout" class="auth-button logout-button">ログアウト</button>
          </template>
          <template v-else>
            <button @click="login" class="auth-button login-button">ログイン</button>
          </template>
        </div>
      </nav>
    </header>
    <main>
      <router-view />
    </main>
  </div>
</template>

<script lang="ts">
import { defineComponent, computed, onMounted } from 'vue';
import { useStore } from 'vuex';

export default defineComponent({
  name: 'App',
  setup() {
    const store = useStore();

    // 認証状態を取得
    const isAuthenticated = computed(() => store.getters['auth/isAuthenticated']);
    const currentUser = computed(() => store.getters['auth/currentUser']);

    // ユーザー名を取得する関数
    const getUserName = () => {
      const user = currentUser.value;
      // バックエンドの応答形式に基づいてユーザー名を抽出
      if (user) {
        return user.name || user.username || user.id || 'ユーザー';
      }
      return 'ゲスト';
    };

    // ページロード時に認証状態をチェック
    onMounted(() => {
      store.dispatch('auth/checkAuth');
    });

    // ログイン処理
    const login = async () => {
      try {
        await store.dispatch('auth/login');
      } catch (error) {
        console.error('ログイン処理中にエラーが発生しました:', error);
      }
    };

    // ログアウト処理
    const logout = () => {
      store.dispatch('auth/logout');
    };

    return {
      isAuthenticated,
      currentUser,
      getUserName,
      login,
      logout
    };
  }
});
</script>

<style>
.app-container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

header {
  margin-bottom: 2rem;
}

nav {
  padding: 1rem 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-links {
  display: flex;
  align-items: center;
}

nav a {
  font-weight: bold;
  padding: 0.5rem 1rem;
}

nav a.router-link-exact-active {
  color: #42b983;
}

main {
  flex: 1;
  width: 100%;
}

.auth-buttons {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.auth-button {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}

.login-button {
  background-color: #42b983;
  color: white;
}

.logout-button {
  background-color: #e74c3c;
  color: white;
}

.welcome-text {
  margin-right: 1rem;
  font-weight: bold;
}
</style> 
<template>
  <div class="my-page">
    <h1>マイページ</h1>
    
    <div class="stats-container">
      <div class="stat-card">
        <div class="stat-value">{{ activeThreadCount }}</div>
        <div class="stat-label">有効なスレッド数</div>
        <div class="stat-icon">📊</div>
      </div>
      
      <div class="stat-card">
        <div class="stat-value">{{ totalMessageCount }}</div>
        <div class="stat-label">総会話数</div>
        <div class="stat-icon">💬</div>
      </div>
      
      <div class="stat-card">
        <div class="stat-value">{{ totalThreadCount }}</div>
        <div class="stat-label">総スレッド数</div>
        <div class="stat-icon">📝</div>
      </div>
    </div>
    
    <div class="threads-section">
      <h2>スレッド一覧</h2>
      <div v-if="loading" class="loading">
        <div class="spinner"></div>
        <p>Loading...</p>
      </div>
      <div v-else-if="threads.length === 0" class="empty-state">
        <p>スレッドがありません。</p>
        <router-link to="/chat" class="button">チャットページへ</router-link>
      </div>
      <div v-else class="thread-list">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>タイトル</th>
              <th>メッセージ数</th>
              <th>最終更新日</th>
              <th>状態</th>
              <th>アクション</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="thread in threads" :key="thread.id">
              <td>{{ thread.id }}</td>
              <td>{{ thread.title }}</td>
              <td>{{ thread.messages.length }}</td>
              <td>{{ formatDate(thread.updatedAt) }}</td>
              <td>
                <span :class="['status', thread.isActive ? 'active' : 'inactive']">
                  {{ thread.isActive ? '有効' : '無効' }}
                </span>
              </td>
              <td>
                <div class="action-buttons">
                  <router-link :to="`/chat`" class="view-btn" @click="selectThread(thread.id)">表示</router-link>
                  <button @click="toggleThreadActive(thread.id)" class="toggle-btn">
                    {{ thread.isActive ? '無効化' : '有効化' }}
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, computed, onMounted } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';

export default defineComponent({
  name: 'MyPage',
  
  setup() {
    const store = useStore();
    const router = useRouter();
    
    // データの取得
    const threads = computed(() => store.getters['chat/allThreads']);
    const loading = computed(() => store.state.chat.loading);
    const totalThreadCount = computed(() => store.getters['chat/totalThreadCount']);
    const activeThreadCount = computed(() => store.getters['chat/activeThreadCount']);
    const totalMessageCount = computed(() => store.getters['chat/totalMessageCount']);
    
    // ページ読み込み時にスレッドをロード
    onMounted(() => {
      store.dispatch('chat/loadThreads');
    });
    
    // スレッドの有効/無効を切り替え
    const toggleThreadActive = (threadId: number) => {
      store.dispatch('chat/toggleThread', threadId);
    };
    
    // スレッドを選択して、チャットページに遷移
    const selectThread = (threadId: number) => {
      store.dispatch('chat/setCurrentThread', threadId);
    };
    
    // 日付フォーマット
    const formatDate = (timestamp: number) => {
      const date = new Date(timestamp);
      return date.toLocaleDateString('ja-JP', { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    };
    
    return {
      threads,
      loading,
      totalThreadCount,
      activeThreadCount,
      totalMessageCount,
      toggleThreadActive,
      selectThread,
      formatDate
    };
  }
});
</script>

<style scoped>
.my-page {
  max-width: 1000px;
  margin: 0 auto;
  padding: 2rem;
}

h1 {
  margin-bottom: 2rem;
  color: #42b983;
  text-align: center;
}

h2 {
  margin: 2rem 0 1rem;
  color: #42b983;
}

/* 統計カード */
.stats-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.stat-card {
  background-color: #f5f5f5;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  position: relative;
  overflow: hidden;
  text-align: center;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.stat-value {
  font-size: 3rem;
  font-weight: bold;
  color: #42b983;
  margin-bottom: 0.5rem;
}

.stat-label {
  font-size: 1.2rem;
  color: #666;
}

.stat-icon {
  position: absolute;
  top: 1rem;
  right: 1rem;
  font-size: 2rem;
  opacity: 0.2;
}

/* スレッドリスト */
.thread-list {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  overflow: hidden;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid #e0e0e0;
}

th {
  background-color: #42b983;
  font-weight: bold;
  color: #ffffff;
}

td {
  color: #000000;
  background-color: #ffffff;
}

tr:hover {
  background-color: #f0f0f0;
}

.status {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 999px;
  font-size: 0.8rem;
  font-weight: bold;
}

.status.active {
  background-color: #42b983;
  color: #ffffff;
}

.status.inactive {
  background-color: #666666;
  color: #ffffff;
}

.action-buttons {
  display: flex;
  gap: 0.5rem;
}

.view-btn, .toggle-btn {
  font-size: 0.8rem;
  padding: 0.4rem 0.8rem;
  border-radius: 4px;
  border: none;
  cursor: pointer;
  font-weight: bold;
}

.view-btn {
  background-color: #42b983;
  color: white;
  text-decoration: none;
}

.toggle-btn {
  background-color: #666666;
  color: white;
}

.loading, .empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem;
  color: #000000;
  text-align: center;
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.spinner {
  border: 4px solid rgba(0, 0, 0, 0.1);
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border-left-color: #42b983;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.button {
  display: inline-block;
  background-color: #42b983;
  color: white;
  padding: 0.8rem 1.5rem;
  border-radius: 4px;
  text-decoration: none;
  margin-top: 1rem;
  font-weight: bold;
}

.button:hover {
  background-color: #3da776;
}
</style> 
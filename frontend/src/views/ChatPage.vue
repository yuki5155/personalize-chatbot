<template>
  <div class="chat-page" :class="[
    settings.darkMode ? 'dark-mode' : '', 
    `font-size-${settings.fontSize}`
  ]">
    <div class="sidebar">
      <div class="sidebar-header">
        <h2>スレッド一覧</h2>
        <button @click="createNewThread" class="new-thread-btn">
          + 新規スレッド
        </button>
      </div>
      <div v-if="loading" class="loading">
        <div class="spinner"></div>
        <p>Loading...</p>
      </div>
      <div v-else-if="threads.length === 0" class="empty-state">
        <p>スレッドがありません。</p>
        <p>新しいスレッドを作成してください。</p>
      </div>
      <div v-else class="thread-list">
        <div
          v-for="thread in threads"
          :key="thread.id"
          :class="['thread-item', { active: currentThreadId === thread.id }]"
          @click="selectThread(thread.id)"
        >
          <div class="thread-item-inner">
            <div class="thread-title">{{ thread.title }}</div>
            <div class="thread-meta">
              <span class="thread-date">{{ formatDate(thread.updatedAt) }}</span>
              <span class="thread-messages">{{ thread.messages.length }}メッセージ</span>
            </div>
          </div>
          <div class="thread-actions">
            <button 
              @click.stop="toggleThreadActive(thread.id)"
              :class="['toggle-btn', thread.isActive ? 'active' : 'inactive']"
              :title="thread.isActive ? '無効化' : '有効化'"
            >
              {{ thread.isActive ? '有効' : '無効' }}
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <div class="chat-container">
      <div v-if="currentThread" class="chat-wrapper">
        <div class="chat-header">
          <h2>{{ currentThread.title }}</h2>
          <div class="header-actions">
            <div v-if="!currentThread.isActive" class="inactive-badge">無効化済み</div>
            <button class="settings-btn" @click="openSettings">
              <span class="settings-icon">⚙️</span>
            </button>
          </div>
        </div>
        
        <ChatArea @new-thread="createNewThread" />
        
        <ChatInputForm 
          :disabled="!currentThread.isActive || isTyping" 
          @send-message="handleSendMessage" 
        />
      </div>
      
      <div v-else class="empty-chat">
        <div class="empty-chat-content">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="empty-icon">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 20.25c4.97 0 9-3.694 9-8.25s-4.03-8.25-9-8.25S3 7.444 3 12c0 2.104.859 4.023 2.273 5.48.432.447.74 1.04.586 1.641a4.483 4.483 0 01-.923 1.785A5.969 5.969 0 006 21c1.282 0 2.47-.402 3.445-1.087.81.22 1.668.337 2.555.337z" />
          </svg>
          <h2>会話を始めましょう</h2>
          <p>左側のメニューから会話を選択するか、新しい会話を始めてください。</p>
          <button @click="createNewThread" class="new-chat-btn">
            新しい会話を始める
          </button>
        </div>
      </div>
    </div>
    
    <!-- 設定モーダル -->
    <SettingsModal 
      :isOpen="isSettingsOpen" 
      @close="closeSettings"
      @save="onSettingsSave"
    />
    
    <!-- 新規スレッド作成モーダル -->
    <NewThreadModal
      :isOpen="isNewThreadModalOpen"
      @close="closeNewThreadModal"
      @create="onNewThreadCreate"
    />
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed, onMounted, reactive } from 'vue';
import { useStore } from 'vuex';
import SettingsModal from '../components/SettingsModal.vue';
import NewThreadModal from '../components/NewThreadModal.vue';
import ChatArea from '../components/ChatArea.vue';
import ChatInputForm from '../components/ChatInputForm.vue';

export default defineComponent({
  name: 'ChatPage',
  
  components: {
    SettingsModal,
    NewThreadModal,
    ChatArea,
    ChatInputForm
  },
  
  setup() {
    const store = useStore();
    const isSettingsOpen = ref(false);
    const isNewThreadModalOpen = ref(false);
    
    // 設定の状態を保持
    const settings = reactive({
      darkMode: false,
      fontSize: 'medium',
      notifications: true,
      notificationSound: true
    });
    
    // ストアからのデータ取得
    const threads = computed(() => store.getters['chat/allThreads']);
    const currentThreadId = computed(() => store.state.chat.currentThreadId);
    const currentThread = computed(() => store.getters['chat/currentThread']);
    const loading = computed(() => store.state.chat.loading);
    const isTyping = computed(() => store.getters['chat/isTyping']);
    
    // 設定を読み込む
    const loadSettings = () => {
      const savedSettings = store.getters['settings/getSettings'];
      if (savedSettings) {
        settings.darkMode = savedSettings.darkMode;
        settings.fontSize = savedSettings.fontSize;
        settings.notifications = savedSettings.notifications;
        settings.notificationSound = savedSettings.notificationSound;
      }
    };
    
    // ページ読み込み時にスレッドと設定をロード
    onMounted(() => {
      store.dispatch('chat/loadThreads');
      store.dispatch('settings/loadSettings').then(() => {
        loadSettings();
      });
    });
    
    // 新規スレッド作成モーダルを開く
    const createNewThread = () => {
      isNewThreadModalOpen.value = true;
    };
    
    // 新規スレッド作成モーダルを閉じる
    const closeNewThreadModal = () => {
      isNewThreadModalOpen.value = false;
    };
    
    // 新規スレッド作成処理
    const onNewThreadCreate = ({ title, firstMessage }: { title: string, firstMessage: string }) => {
      store.dispatch('chat/createThread', { title, firstMessage });
      closeNewThreadModal();
    };
    
    // スレッド選択
    const selectThread = (threadId: number) => {
      store.dispatch('chat/setCurrentThread', threadId);
    };
    
    // スレッド有効・無効切り替え
    const toggleThreadActive = (threadId: number) => {
      store.dispatch('chat/toggleThread', threadId);
    };
    
    // 設定モーダルを開く
    const openSettings = () => {
      isSettingsOpen.value = true;
    };
    
    // 設定モーダルを閉じる
    const closeSettings = () => {
      isSettingsOpen.value = false;
    };
    
    // 設定保存時の処理
    const onSettingsSave = (newSettings: any) => {
      // 設定を更新
      settings.darkMode = newSettings.darkMode;
      settings.fontSize = newSettings.fontSize;
      settings.notifications = newSettings.notifications;
      settings.notificationSound = newSettings.notificationSound;
      
      // ストアに設定を保存
      store.dispatch('settings/saveSettings', newSettings);
      
      // モーダルを閉じる
      closeSettings();
    };
    
    // メッセージを送信
    const handleSendMessage = (text: string) => {
      // ストリーミングレスポンスを使う場合はこちらを使用
      store.dispatch('chat/sendMessageWithStreamingResponse', text);
      
      // 通常のレスポンスを使う場合はこちらを使用
      // store.dispatch('chat/sendMessage', text);
    };
    
    // 日付フォーマット
    const formatDate = (timestamp: number) => {
      const date = new Date(timestamp);
      return date.toLocaleDateString();
    };
    
    // 時刻フォーマット
    const formatTime = (timestamp: number) => {
      const date = new Date(timestamp);
      return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    };
    
    return {
      threads,
      currentThreadId,
      currentThread,
      loading,
      isTyping,
      isSettingsOpen,
      isNewThreadModalOpen,
      settings,
      createNewThread,
      closeNewThreadModal,
      onNewThreadCreate,
      selectThread,
      toggleThreadActive,
      openSettings,
      closeSettings,
      onSettingsSave,
      handleSendMessage,
      formatDate,
      formatTime
    };
  }
});
</script>

<style scoped>
.chat-page {
  display: flex;
  height: calc(100vh - 60px);
  background-color: #ffffff;
  color: #1f2937;
}

.dark-mode {
  background-color: #1f2937;
  color: #e5e7eb;
}

.sidebar {
  width: 300px;
  border-right: 1px solid #e5e7eb;
  display: flex;
  flex-direction: column;
  height: 100%;
  background-color: #f9fafb;
}

.dark-mode .sidebar {
  background-color: #111827;
  border-right-color: #374151;
}

.sidebar-header {
  padding: 16px;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.dark-mode .sidebar-header {
  border-bottom-color: #374151;
}

.new-thread-btn {
  background-color: #4f46e5;
  color: white;
  border: none;
  padding: 8px 12px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
}

.new-thread-btn:hover {
  background-color: #4338ca;
}

.thread-list {
  overflow-y: auto;
  flex: 1;
}

.thread-item {
  padding: 12px 16px;
  border-bottom: 1px solid #e5e7eb;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
}

.dark-mode .thread-item {
  border-bottom-color: #374151;
}

.thread-item:hover {
  background-color: #f3f4f6;
}

.dark-mode .thread-item:hover {
  background-color: #1e293b;
}

.thread-item.active {
  background-color: #e0e7ff;
}

.dark-mode .thread-item.active {
  background-color: #312e81;
}

.thread-item-inner {
  flex: 1;
  min-width: 0;
}

.thread-title {
  font-weight: 500;
  margin-bottom: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.thread-meta {
  display: flex;
  font-size: 0.8rem;
  color: #6b7280;
}

.dark-mode .thread-meta {
  color: #9ca3af;
}

.thread-date {
  margin-right: 8px;
}

.thread-actions {
  display: flex;
  align-items: center;
}

.toggle-btn {
  font-size: 0.7rem;
  padding: 2px 6px;
  border-radius: 4px;
  border: none;
  cursor: pointer;
}

.toggle-btn.active {
  background-color: #10b981;
  color: white;
}

.toggle-btn.inactive {
  background-color: #ef4444;
  color: white;
}

.loading, .empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #6b7280;
  text-align: center;
  padding: 20px;
}

.dark-mode .loading, .dark-mode .empty-state {
  color: #9ca3af;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(79, 70, 229, 0.1);
  border-left-color: #4f46e5;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.chat-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.chat-wrapper {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.chat-header {
  padding: 16px;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.dark-mode .chat-header {
  border-bottom-color: #374151;
}

.header-actions {
  display: flex;
  align-items: center;
}

.inactive-badge {
  background-color: #ef4444;
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.8rem;
  margin-right: 8px;
}

.settings-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.5rem;
}

.empty-chat {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
}

.empty-chat-content {
  text-align: center;
  max-width: 400px;
}

.empty-icon {
  width: 64px;
  height: 64px;
  color: #9ca3af;
  margin: 0 auto 16px;
}

.new-chat-btn {
  background-color: #4f46e5;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  margin-top: 16px;
}

.new-chat-btn:hover {
  background-color: #4338ca;
}

/* レスポンシブデザイン */
@media (max-width: 768px) {
  .chat-page {
    flex-direction: column;
  }
  
  .sidebar {
    width: 100%;
    height: auto;
    max-height: 40vh;
  }
}

/* フォントサイズ設定 */
.font-size-small {
  font-size: 0.9rem;
}

.font-size-medium {
  font-size: 1rem;
}

.font-size-large {
  font-size: 1.1rem;
}
</style> 
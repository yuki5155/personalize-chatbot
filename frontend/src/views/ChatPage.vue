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
      <div v-if="!currentThread" class="no-thread-selected">
        <h2>スレッドを選択するか、新しいスレッドを作成してください</h2>
      </div>
      <div v-else class="chat-area">
        <div class="chat-header">
          <h2>{{ currentThread.title }}</h2>
          <div class="header-actions">
            <div v-if="!currentThread.isActive" class="inactive-badge">無効化済み</div>
            <button class="settings-btn" @click="openSettings">
              <span class="settings-icon">⚙️</span>
            </button>
          </div>
        </div>
        <div :class="['messages', { 'inactive-thread': !currentThread.isActive }]">
          <div v-if="currentThread.messages.length === 0" class="empty-messages">
            <p>メッセージがありません。</p>
            <p>最初のメッセージを送信してください。</p>
          </div>
          <div 
            v-for="message in currentThread.messages" 
            :key="message.id"
            :class="['message', message.sender]"
          >
            <div class="message-content">
              <div class="message-text">{{ message.text }}</div>
              <div class="message-time">{{ formatTime(message.timestamp) }}</div>
            </div>
          </div>
        </div>
        <div class="message-input">
          <div class="preset-buttons">
            <button 
              v-for="(preset, index) in presets" 
              :key="index" 
              @click="usePreset(preset)"
              :disabled="!currentThread || !currentThread.isActive"
              class="preset-button"
            >
              {{ preset.label }}
            </button>
          </div>
          <form @submit.prevent="sendMessage">
            <input 
              v-model="newMessage" 
              placeholder="メッセージを入力..." 
              :disabled="!currentThread || !currentThread.isActive"
            />
            <button type="submit" :disabled="!newMessage || !currentThread || !currentThread.isActive">送信</button>
          </form>
          <div v-if="currentThread && !currentThread.isActive" class="inactive-thread-notice">
            このスレッドは無効化されています。メッセージを送信するには、スレッドを有効化してください。
          </div>
        </div>
      </div>
    </div>
    
    <!-- 設定モーダル -->
    <SettingsModal 
      :isOpen="isSettingsOpen" 
      @close="closeSettings"
      @save="onSettingsSave"
    />
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed, onMounted, reactive } from 'vue';
import { useStore } from 'vuex';
import SettingsModal from '../components/SettingsModal.vue';

export default defineComponent({
  name: 'ChatPage',
  
  components: {
    SettingsModal
  },
  
  setup() {
    const store = useStore();
    const newMessage = ref('');
    const newThreadTitle = ref('');
    const isSettingsOpen = ref(false);
    
    // 設定の状態を保持
    const settings = reactive({
      darkMode: false,
      fontSize: 'medium',
      notifications: true,
      notificationSound: true
    });
    
    // プリセットメッセージの定義
    const presets = reactive([
      { label: '自己紹介', text: 'こんにちは！あなたについて教えてください。' },
      { label: '機能説明', text: 'このチャットボットでできることを教えてください。' },
      { label: 'ヘルプ', text: '使い方について教えてください。' },
      { label: '雑談', text: '今日の天気はどうですか？' }
    ]);
    
    // ストアからのデータ取得
    const threads = computed(() => store.getters['chat/allThreads']);
    const currentThreadId = computed(() => store.state.chat.currentThreadId);
    const currentThread = computed(() => store.getters['chat/currentThread']);
    const loading = computed(() => store.state.chat.loading);
    
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
    
    // 新規スレッド作成
    const createNewThread = () => {
      const title = prompt('新しいスレッドのタイトルを入力してください:', `新しいスレッド ${threads.value.length + 1}`);
      if (title) {
        store.dispatch('chat/createThread', title);
      }
    };
    
    // スレッド選択
    const selectThread = (threadId: number) => {
      store.dispatch('chat/setCurrentThread', threadId);
    };
    
    // メッセージ送信
    const sendMessage = () => {
      if (newMessage.value && currentThreadId.value) {
        store.dispatch('chat/sendMessage', newMessage.value);
        newMessage.value = '';
      }
    };
    
    // スレッドの有効/無効を切り替え
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
    
    // 設定が保存されたときの処理
    const onSettingsSave = (newSettings: any) => {
      console.log('設定が保存されました:', newSettings);
      // 設定を反映
      settings.darkMode = newSettings.darkMode;
      settings.fontSize = newSettings.fontSize;
      settings.notifications = newSettings.notifications;
      settings.notificationSound = newSettings.notificationSound;
    };
    
    // プリセットメッセージを使用する
    const usePreset = (preset: { label: string, text: string }) => {
      newMessage.value = preset.text;
    };
    
    // 日付フォーマット
    const formatDate = (timestamp: number) => {
      const date = new Date(timestamp);
      return date.toLocaleDateString('ja-JP');
    };
    
    // 時刻フォーマット
    const formatTime = (timestamp: number) => {
      const date = new Date(timestamp);
      return date.toLocaleTimeString('ja-JP', { hour: '2-digit', minute: '2-digit' });
    };
    
    return {
      threads,
      currentThreadId,
      currentThread,
      loading,
      newMessage,
      isSettingsOpen,
      settings,
      presets,
      usePreset,
      createNewThread,
      selectThread,
      sendMessage,
      toggleThreadActive,
      openSettings,
      closeSettings,
      onSettingsSave,
      formatDate,
      formatTime
    };
  }
});
</script>

<style scoped>
.chat-page {
  display: flex;
  width: 100%;
  height: calc(100vh - 150px);
  min-height: 500px;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.sidebar {
  width: 300px;
  background-color: #e0e0e0;
  border-right: 1px solid #d0d0d0;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.sidebar-header {
  padding: 1rem;
  border-bottom: 1px solid #e0e0e0;
}

.sidebar-header h2 {
  color: #000000;
  font-weight: bold;
}

.new-thread-btn {
  background-color: #42b983;
  color: white;
  border: none;
  width: 100%;
  padding: 0.5rem;
  margin-top: 0.5rem;
  cursor: pointer;
  border-radius: 4px;
  font-weight: 600;
}

.thread-list {
  flex: 1;
  overflow-y: auto;
}

.thread-item {
  padding: 1rem;
  border-bottom: 1px solid #d0d0d0;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #e8e8e8;
}

.thread-item:hover {
  background-color: #d5d5d5;
}

.thread-item.active {
  background-color: #c8e9d8;
  border-left: 4px solid #42b983;
}

.thread-title {
  font-weight: 700;
  margin-bottom: 0.5rem;
  color: #000000;
  letter-spacing: 0.02em;
}

.thread-item.active .thread-title {
  color: #096144;
}

.thread-meta {
  font-size: 0.8rem;
  color: #000000;
  display: flex;
  justify-content: space-between;
}

.toggle-btn {
  font-size: 0.7rem;
  padding: 0.2rem 0.5rem;
  border-radius: 10px;
  border: none;
  cursor: pointer;
  font-weight: 600;
}

.toggle-btn.active {
  background-color: #42b983;
  color: white;
}

.toggle-btn.inactive {
  background-color: #999;
  color: white;
}

.chat-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  background-color: white;
}

.no-thread-selected {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100%;
  color: #333;
  text-align: center;
  padding: 2rem;
}

.no-thread-selected h2 {
  color: #000000;
  font-weight: bold;
}

.chat-header {
  padding: 1rem;
  border-bottom: 1px solid #e0e0e0;
  background-color: #e0e0e0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chat-header h2 {
  color: #000000;
  font-weight: 700;
  margin: 0;
  font-size: 1.2rem;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.inactive-badge {
  background-color: #e74c3c;
  color: white;
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: bold;
}

.settings-btn {
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background-color 0.2s;
}

.settings-btn:hover {
  background-color: #f0f0f0;
}

.settings-icon {
  font-size: 1.2rem;
}

.messages {
  flex: 1;
  padding: 1rem;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}

.messages.inactive-thread {
  background-color: rgba(231, 76, 60, 0.05);
  position: relative;
}

.messages.inactive-thread::after {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(240, 240, 240, 0.5);
  pointer-events: none;
}

.message {
  max-width: 80%;
  margin-bottom: 1rem;
  padding: 0.8rem;
  border-radius: 10px;
  position: relative;
}

.message.user {
  align-self: flex-end;
  background-color: #42b983;
  color: white;
}

.message.assistant {
  align-self: flex-start;
  background-color: #e0e0e0;
  color: #000000;
}

.message-text {
  margin-bottom: 0.3rem;
}

.message-time {
  font-size: 0.7rem;
  opacity: 0.7;
  text-align: right;
}

.message-input {
  padding: 1rem;
  border-top: 1px solid #e0e0e0;
}

.message-input form {
  display: flex;
}

.message-input input {
  flex: 1;
  padding: 0.8rem;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  margin-right: 0.5rem;
}

.message-input button {
  background-color: #42b983;
  color: white;
  border: none;
  padding: 0 1.5rem;
  border-radius: 4px;
  cursor: pointer;
}

.message-input button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.inactive-thread-notice {
  margin-top: 0.5rem;
  color: #e74c3c;
  font-size: 0.8rem;
  text-align: center;
  padding: 0.5rem;
  background-color: #fadbd8;
  border-radius: 4px;
}

.loading, .empty-state, .empty-messages {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  color: #000000;
  text-align: center;
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

.chat-area {
  display: flex;
  flex-direction: column;
  height: 100%;
}

/* ダークモード */
.dark-mode {
  background-color: #1a1a1a;
  color: #f5f5f5;
}

.dark-mode .sidebar {
  background-color: #262626;
  border-right-color: #333;
}

.dark-mode .sidebar-header {
  border-bottom-color: #333;
}

.dark-mode .sidebar-header h2 {
  color: #f5f5f5;
}

.dark-mode .thread-item {
  border-bottom-color: #333;
}

.dark-mode .thread-item:hover {
  background-color: #333;
}

.dark-mode .thread-item.active {
  background-color: rgba(66, 185, 131, 0.2);
}

.dark-mode .thread-title {
  color: #f5f5f5;
}

.dark-mode .thread-meta {
  color: #aaa;
}

.dark-mode .chat-container {
  background-color: #1a1a1a;
}

.dark-mode .chat-header {
  background-color: #262626;
  border-bottom-color: #333;
}

.dark-mode .message.assistant {
  background-color: #333;
  color: #f5f5f5;
}

.dark-mode .message-input input {
  background-color: #333;
  color: #f5f5f5;
  border-color: #444;
}

.dark-mode .message-input input::placeholder {
  color: #aaa;
}

.dark-mode .no-thread-selected h2,
.dark-mode .empty-messages p,
.dark-mode .empty-state p {
  color: #f5f5f5;
}

/* 文字サイズ */
.font-size-small {
  font-size: 0.9rem;
}

.font-size-medium {
  font-size: 1rem;
}

.font-size-large {
  font-size: 1.2rem;
}

.font-size-small .message {
  font-size: 0.9rem;
}

.font-size-medium .message {
  font-size: 1rem;
}

.font-size-large .message {
  font-size: 1.2rem;
}

.font-size-small .thread-title {
  font-size: 0.9rem;
}

.font-size-medium .thread-title {
  font-size: 1rem;
}

.font-size-large .thread-title {
  font-size: 1.1rem;
}

.preset-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 10px;
}

.preset-button {
  background-color: #f0f0f0;
  border: 1px solid #ddd;
  border-radius: 16px;
  padding: 6px 12px;
  font-size: 0.9em;
  cursor: pointer;
  transition: all 0.2s ease;
}

.preset-button:hover {
  background-color: #e0e0e0;
}

.preset-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.dark-mode .preset-button {
  background-color: #444;
  border-color: #555;
  color: #ddd;
}

.dark-mode .preset-button:hover {
  background-color: #555;
}
</style> 
<template>
  <div class="chat-area">
    <div v-if="loading" class="loading-container">
      <div class="loading-spinner"></div>
      <p>メッセージを読み込み中...</p>
    </div>
    
    <div v-else-if="!currentThread" class="empty-state">
      <div class="empty-icon">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="icon">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 20.25c4.97 0 9-3.694 9-8.25s-4.03-8.25-9-8.25S3 7.444 3 12c0 2.104.859 4.023 2.273 5.48.432.447.74 1.04.586 1.641a4.483 4.483 0 01-.923 1.785A5.969 5.969 0 006 21c1.282 0 2.47-.402 3.445-1.087.81.22 1.668.337 2.555.337z" />
        </svg>
      </div>
      <h3>会話がありません</h3>
      <p>左側のメニューから会話を選択するか、新しい会話を始めてください。</p>
      <button @click="$emit('new-thread')" class="new-chat-btn">
        新しい会話を始める
      </button>
    </div>
    
    <div v-else class="messages-container" ref="messagesContainerRef">
      <div v-if="currentThread.messages.length === 0" class="empty-messages">
        <p>この会話はまだメッセージがありません。</p>
        <p>「{{ currentThread.title }}」について質問してみましょう。</p>
      </div>
      
      <template v-else>
        <ChatMessage
          v-for="message in currentThread.messages"
          :key="message.id"
          :message="message"
        />
      </template>
      
      <div v-if="isTyping" class="typing-indicator">
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, computed, ref, watch, nextTick } from 'vue';
import { useStore } from 'vuex';
import ChatMessage from './ChatMessage.vue';

export default defineComponent({
  name: 'ChatArea',
  components: {
    ChatMessage
  },
  
  emits: ['new-thread'],
  
  setup() {
    const store = useStore();
    const messagesContainerRef = ref<HTMLElement | null>(null);
    
    // チャット画面の状態をStoreから取得
    const currentThread = computed(() => store.getters['chat/currentThread']);
    const isTyping = computed(() => store.getters['chat/isTyping']);
    const loading = computed(() => store.getters['chat/isLoading']);
    
    // メッセージが追加されたらスクロールを一番下に移動
    const scrollToBottom = () => {
      nextTick(() => {
        if (messagesContainerRef.value) {
          messagesContainerRef.value.scrollTop = messagesContainerRef.value.scrollHeight;
        }
      });
    };
    
    // メッセージが変更されたらスクロールを下に移動
    watch(
      () => currentThread.value?.messages?.length,
      () => scrollToBottom(),
      { immediate: true }
    );
    
    // 入力中状態が変わったらスクロールを下に移動
    watch(
      () => isTyping.value,
      () => scrollToBottom()
    );
    
    return {
      currentThread,
      isTyping,
      loading,
      messagesContainerRef
    };
  }
});
</script>

<style scoped>
.chat-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  background-color: #f9fafb;
  border-radius: 12px;
  overflow: hidden;
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  scroll-behavior: smooth;
}

.empty-state {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  text-align: center;
  color: #6b7280;
}

.empty-icon {
  width: 64px;
  height: 64px;
  color: #9ca3af;
  margin-bottom: 1rem;
}

.empty-state h3 {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #374151;
}

.empty-state p {
  margin-bottom: 1.5rem;
  max-width: 400px;
}

.new-chat-btn {
  background-color: #4f46e5;
  color: white;
  border: none;
  padding: 0.75rem 1.25rem;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.new-chat-btn:hover {
  background-color: #4338ca;
}

.empty-messages {
  text-align: center;
  color: #6b7280;
  padding: 2rem;
}

.loading-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(79, 70, 229, 0.1);
  border-left-color: #4f46e5;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

.typing-indicator {
  display: flex;
  padding: 12px 16px;
  width: fit-content;
  border-radius: 24px;
  background-color: #e5e7eb;
  margin-left: 48px;
  margin-bottom: 16px;
}

.typing-dot {
  width: 8px;
  height: 8px;
  background-color: #6b7280;
  border-radius: 50%;
  margin: 0 4px;
  animation: bounce 1.5s infinite;
}

.typing-dot:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-dot:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@keyframes bounce {
  0%, 60%, 100% { transform: translateY(0); }
  30% { transform: translateY(-6px); }
}
</style> 
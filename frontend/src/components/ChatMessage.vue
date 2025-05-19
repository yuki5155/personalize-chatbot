<template>
  <div class="message" :class="{ 'message-user': isUser, 'message-assistant': !isUser }">
    <div class="message-avatar">
      <div class="avatar" :class="{ 'avatar-user': isUser, 'avatar-assistant': !isUser }">
        {{ isUser ? 'U' : 'A' }}
      </div>
    </div>
    <div class="message-content">
      <div class="message-header">
        <span class="message-sender">{{ isUser ? 'You' : 'Assistant' }}</span>
        <span class="message-time">{{ formattedTime }}</span>
      </div>
      <div class="message-text" v-html="formattedText"></div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, computed } from 'vue';
import { Message } from '../store/modules/chat';

export default defineComponent({
  name: 'ChatMessage',
  props: {
    message: {
      type: Object as () => Message,
      required: true
    }
  },
  setup(props) {
    // ユーザーのメッセージかどうか
    const isUser = computed(() => props.message.sender === 'user');
    
    // フォーマット済みの時間
    const formattedTime = computed(() => {
      const date = new Date(props.message.timestamp);
      return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    });
    
    // テキスト内のURLをリンクに変換
    const formattedText = computed(() => {
      const urlRegex = /(https?:\/\/[^\s]+)/g;
      return props.message.text.replace(urlRegex, url => `<a href="${url}" target="_blank" rel="noopener noreferrer">${url}</a>`);
    });
    
    return {
      isUser,
      formattedTime,
      formattedText
    };
  }
});
</script>

<style scoped>
.message {
  display: flex;
  margin-bottom: 16px;
  animation: fadeIn 0.3s;
}

.message-user {
  flex-direction: row-reverse;
}

.message-avatar {
  margin: 0 12px;
}

.avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  color: white;
}

.avatar-user {
  background-color: #4f46e5;
}

.avatar-assistant {
  background-color: #10b981;
}

.message-content {
  max-width: 70%;
  padding: 12px;
  border-radius: 8px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.message-user .message-content {
  background-color: #4f46e5;
  color: white;
  border-radius: 12px 12px 0 12px;
}

.message-assistant .message-content {
  background-color: #f3f4f6;
  color: #1f2937;
  border-radius: 12px 12px 12px 0;
}

.message-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 4px;
  font-size: 0.8rem;
}

.message-user .message-header {
  color: rgba(255, 255, 255, 0.8);
}

.message-text {
  line-height: 1.5;
  word-break: break-word;
}

.message-text a {
  color: inherit;
  text-decoration: underline;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style> 
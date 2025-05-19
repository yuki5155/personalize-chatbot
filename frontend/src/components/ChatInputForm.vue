<template>
  <div class="chat-input-form">
    <form @submit.prevent="submitMessage">
      <div class="input-container">
        <textarea
          ref="textareaRef"
          v-model="message"
          placeholder="メッセージを入力..."
          :disabled="disabled"
          @keydown.enter.prevent="onEnterPress"
          @input="autoResize"
        ></textarea>
        <button 
          type="submit" 
          class="send-button" 
          :disabled="!canSubmit"
        >
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="icon">
            <path d="M3.478 2.405a.75.75 0 00-.926.94l2.432 7.905H13.5a.75.75 0 010 1.5H4.984l-2.432 7.905a.75.75 0 00.926.94 60.519 60.519 0 0018.445-8.986.75.75 0 000-1.218A60.517 60.517 0 003.478 2.405z" />
          </svg>
        </button>
      </div>
      <div class="hints">
        <span v-if="disabled" class="disabled-hint">応答を待っています...</span>
        <span v-else-if="!message.trim()" class="hint">Enterキーで送信、Shift+Enterで改行</span>
        <span v-else class="char-count">{{ message.length }} / 1000文字</span>
      </div>
    </form>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed, onMounted, nextTick } from 'vue';

export default defineComponent({
  name: 'ChatInputForm',
  props: {
    disabled: {
      type: Boolean,
      default: false
    },
    maxLength: {
      type: Number,
      default: 1000
    }
  },
  
  emits: ['send-message'],
  
  setup(props, { emit }) {
    const message = ref('');
    const textareaRef = ref<HTMLTextAreaElement | null>(null);
    
    const canSubmit = computed(() => {
      return message.value.trim().length > 0 && 
             message.value.length <= props.maxLength &&
             !props.disabled;
    });
    
    // エンターキーハンドラー
    const onEnterPress = (e: KeyboardEvent) => {
      // Shift+Enterなら改行を許可
      if (e.shiftKey) return;
      
      // 通常のEnterはメッセージ送信
      if (canSubmit.value) {
        submitMessage();
      }
    };
    
    // メッセージ送信
    const submitMessage = () => {
      if (!canSubmit.value) return;
      
      emit('send-message', message.value);
      message.value = '';
      
      // 入力エリアのサイズをリセット
      nextTick(() => {
        if (textareaRef.value) {
          textareaRef.value.style.height = 'auto';
        }
      });
    };
    
    // テキストエリアの高さを自動調整
    const autoResize = () => {
      const textarea = textareaRef.value;
      if (!textarea) return;
      
      textarea.style.height = 'auto';
      textarea.style.height = `${Math.min(textarea.scrollHeight, 200)}px`;
    };
    
    // コンポーネント初期化時にフォーカス
    onMounted(() => {
      if (textareaRef.value) {
        textareaRef.value.focus();
      }
    });
    
    return {
      message,
      textareaRef,
      canSubmit,
      onEnterPress,
      submitMessage,
      autoResize
    };
  }
});
</script>

<style scoped>
.chat-input-form {
  background-color: #ffffff;
  border-top: 1px solid #e5e7eb;
  padding: 12px 16px;
  border-radius: 0 0 12px 12px;
}

.input-container {
  display: flex;
  position: relative;
}

textarea {
  flex: 1;
  border: 1px solid #d1d5db;
  border-radius: 24px;
  padding: 12px 50px 12px 16px;
  resize: none;
  min-height: 48px;
  max-height: 200px;
  overflow-y: auto;
  font-family: inherit;
  font-size: 0.95rem;
  line-height: 1.5;
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s;
}

textarea:focus {
  border-color: #4f46e5;
  box-shadow: 0 0 0 2px rgba(79, 70, 229, 0.2);
}

textarea:disabled {
  background-color: #f9fafb;
  cursor: not-allowed;
}

.send-button {
  position: absolute;
  right: 6px;
  bottom: 6px;
  background-color: #4f46e5;
  color: white;
  border: none;
  border-radius: 50%;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background-color 0.2s;
}

.send-button:hover:not(:disabled) {
  background-color: #4338ca;
}

.send-button:disabled {
  background-color: #9ca3af;
  cursor: not-allowed;
}

.icon {
  width: 20px;
  height: 20px;
}

.hints {
  margin-top: 4px;
  font-size: 0.75rem;
  color: #6b7280;
  text-align: right;
  padding: 0 8px;
}

.disabled-hint {
  color: #ef4444;
  font-weight: 500;
}

.char-count {
  color: #4b5563;
}
</style> 
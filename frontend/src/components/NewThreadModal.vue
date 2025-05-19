<template>
  <transition name="modal-fade">
    <div v-if="isOpen" class="modal-overlay">
      <div class="modal-content">
        <div class="modal-header">
          <h3>新規スレッド作成</h3>
          <button class="close-btn" @click="$emit('close')" aria-label="閉じる">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="createThread">
            <div class="form-group">
              <label for="thread-title">スレッドタイトル</label>
              <input 
                id="thread-title" 
                v-model="title" 
                type="text" 
                placeholder="タイトルを入力してください" 
                required
                autocomplete="off"
              />
            </div>
            <div class="form-group">
              <label for="first-message">最初のメッセージ</label>
              <textarea 
                id="first-message" 
                v-model="firstMessage" 
                placeholder="最初のメッセージを入力してください" 
                rows="4" 
                required
              ></textarea>
            </div>
            <div class="form-actions">
              <button type="button" class="cancel-btn" @click="$emit('close')">キャンセル</button>
              <button type="submit" class="create-btn" :disabled="!title || !firstMessage">
                <svg v-if="!title || !firstMessage" class="icon" width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M12 5V19M5 12H19" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                作成する
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </transition>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';

export default defineComponent({
  name: 'NewThreadModal',
  
  props: {
    isOpen: {
      type: Boolean,
      required: true
    }
  },
  
  emits: ['close', 'create'],
  
  setup(props, { emit }) {
    const title = ref('');
    const firstMessage = ref('');
    
    const createThread = () => {
      if (title.value && firstMessage.value) {
        emit('create', {
          title: title.value,
          firstMessage: firstMessage.value
        });
        // フォームをリセット
        title.value = '';
        firstMessage.value = '';
      }
    };
    
    return {
      title,
      firstMessage,
      createThread
    };
  }
});
</script>

<style scoped>
/* アニメーション */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: all 0.3s ease;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}

.modal-fade-enter-from .modal-content,
.modal-fade-leave-to .modal-content {
  transform: translateY(20px);
  opacity: 0;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(4px);
}

.modal-content {
  background-color: white;
  border-radius: 12px;
  width: 90%;
  max-width: 550px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
  overflow: hidden;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 18px 24px;
  border-bottom: 1px solid #eee;
  background-color: #f9f9f9;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: #333;
}

.close-btn {
  background: none;
  border: none;
  padding: 4px;
  cursor: pointer;
  color: #666;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.close-btn:hover {
  background-color: #f0f0f0;
  color: #333;
}

.modal-body {
  padding: 24px;
  box-sizing: border-box;
}

.form-group {
  margin-bottom: 24px;
  width: 100%;
  box-sizing: border-box;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #444;
  font-size: 0.9rem;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #c8d0d9;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.2s ease;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.05);
  background-color: #fff;
  box-sizing: border-box;
  color: #333;
}

.form-group input:focus,
.form-group textarea:focus {
  border-color: #007bff;
  box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.15);
  outline: none;
}

.form-group input::placeholder,
.form-group textarea::placeholder {
  color: #aaa;
  opacity: 1;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 24px;
}

.cancel-btn,
.create-btn {
  padding: 10px 20px;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s ease;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 8px;
}

.cancel-btn {
  background-color: #f5f5f5;
  border: 1px solid #ddd;
  color: #555;
}

.cancel-btn:hover {
  background-color: #eaeaea;
  color: #333;
}

.create-btn {
  background-color: #007bff;
  border: 1px solid #007bff;
  color: white;
}

.create-btn:hover:not(:disabled) {
  background-color: #0069d9;
  border-color: #0062cc;
}

.create-btn:disabled {
  background-color: #b3d7ff;
  border-color: #b3d7ff;
  cursor: not-allowed;
  opacity: 0.7;
}

.icon {
  display: inline-block;
  vertical-align: middle;
}

/* ダークモード対応 */
:deep(.dark-mode) .modal-content {
  background-color: #2a2a2a;
  color: #f5f5f5;
}

:deep(.dark-mode) .modal-header {
  background-color: #333;
  border-bottom-color: #444;
}

:deep(.dark-mode) .modal-header h3 {
  color: #f5f5f5;
}

:deep(.dark-mode) .close-btn {
  color: #bbb;
}

:deep(.dark-mode) .close-btn:hover {
  background-color: #444;
  color: #fff;
}

:deep(.dark-mode) .form-group label {
  color: #ddd;
}

:deep(.dark-mode) .form-group input,
:deep(.dark-mode) .form-group textarea {
  background-color: #3a3a3a;
  border-color: #555;
  border-width: 2px;
  color: #f5f5f5;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.2);
}

:deep(.dark-mode) .form-group input:focus,
:deep(.dark-mode) .form-group textarea:focus {
  border-color: #4d94ff;
  box-shadow: 0 0 0 3px rgba(77, 148, 255, 0.15);
}

:deep(.dark-mode) .form-group input::placeholder,
:deep(.dark-mode) .form-group textarea::placeholder {
  color: #888;
  opacity: 1;
}

:deep(.dark-mode) .cancel-btn {
  background-color: #444;
  border-color: #555;
  color: #ddd;
}

:deep(.dark-mode) .cancel-btn:hover {
  background-color: #555;
  color: #fff;
}

:deep(.dark-mode) .create-btn {
  background-color: #0d6efd;
  border-color: #0d6efd;
}

:deep(.dark-mode) .create-btn:hover:not(:disabled) {
  background-color: #0b5ed7;
  border-color: #0a58ca;
}

:deep(.dark-mode) .create-btn:disabled {
  background-color: #1a4a7c;
  border-color: #1a4a7c;
  opacity: 0.7;
}

@media (max-width: 576px) {
  .modal-content {
    width: 95%;
    max-width: none;
    border-radius: 10px;
  }
  
  .form-actions {
    flex-direction: column-reverse;
  }
  
  .cancel-btn, 
  .create-btn {
    width: 100%;
    justify-content: center;
  }
}

.modal-body form {
  width: 100%;
  box-sizing: border-box;
  color: #333;
}

:deep(.dark-mode) .modal-body form {
  color: #f5f5f5;
}
</style> 
<template>
  <div v-if="isOpen" class="modal-overlay">
    <div class="modal-content">
      <div class="modal-header">
        <h3>新規スレッド作成</h3>
        <button class="close-btn" @click="$emit('close')">×</button>
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
            <button type="submit" class="create-btn" :disabled="!title || !firstMessage">作成</button>
          </div>
        </form>
      </div>
    </div>
  </div>
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
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  border-radius: 8px;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  border-bottom: 1px solid #eee;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.25rem;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #666;
}

.modal-body {
  padding: 20px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 24px;
}

.cancel-btn,
.create-btn {
  padding: 8px 16px;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
}

.cancel-btn {
  background-color: #f5f5f5;
  border: 1px solid #ddd;
  color: #333;
}

.create-btn {
  background-color: #007bff;
  border: 1px solid #007bff;
  color: white;
}

.create-btn:disabled {
  background-color: #ccc;
  border-color: #ccc;
  cursor: not-allowed;
}

/* ダークモード対応 */
:deep(.dark-mode) .modal-content {
  background-color: #2a2a2a;
  color: #f5f5f5;
}

:deep(.dark-mode) .modal-header {
  border-bottom-color: #444;
}

:deep(.dark-mode) .close-btn {
  color: #ccc;
}

:deep(.dark-mode) .form-group input,
:deep(.dark-mode) .form-group textarea {
  background-color: #333;
  border-color: #555;
  color: #f5f5f5;
}

:deep(.dark-mode) .cancel-btn {
  background-color: #444;
  border-color: #555;
  color: #f5f5f5;
}
</style> 
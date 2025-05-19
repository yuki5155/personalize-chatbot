<template>
  <transition name="modal-fade">
    <div v-if="isOpen" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>チャット設定</h3>
          <button class="close-btn" @click="closeModal" aria-label="閉じる">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
        </div>
        <div class="modal-body">
          <div class="settings-section">
            <h4>表示設定</h4>
            <div class="setting-item">
              <label for="darkMode">
                <span class="setting-label">ダークモード</span>
                <span class="setting-description">画面を暗いテーマに切り替えます</span>
              </label>
              <div class="toggle-switch">
                <input 
                  type="checkbox" 
                  id="darkMode" 
                  v-model="settings.darkMode"
                />
                <span class="toggle-slider"></span>
              </div>
            </div>
            <div class="setting-item">
              <label for="fontSize">
                <span class="setting-label">文字サイズ</span>
                <span class="setting-description">テキストの表示サイズを変更します</span>
              </label>
              <select id="fontSize" v-model="settings.fontSize">
                <option value="small">小</option>
                <option value="medium">中</option>
                <option value="large">大</option>
              </select>
            </div>
          </div>
          
          <div class="settings-section">
            <h4>通知設定</h4>
            <div class="setting-item">
              <label for="notifications">
                <span class="setting-label">通知を有効にする</span>
                <span class="setting-description">新着メッセージの通知を受け取ります</span>
              </label>
              <div class="toggle-switch">
                <input 
                  type="checkbox" 
                  id="notifications" 
                  v-model="settings.notifications"
                />
                <span class="toggle-slider"></span>
              </div>
            </div>
            <div class="setting-item">
              <label for="notificationSound">
                <span class="setting-label">通知音</span>
                <span class="setting-description">新着メッセージ時に音を鳴らします</span>
              </label>
              <div class="toggle-switch">
                <input 
                  type="checkbox" 
                  id="notificationSound" 
                  v-model="settings.notificationSound"
                />
                <span class="toggle-slider"></span>
              </div>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button class="cancel-btn" @click="closeModal">キャンセル</button>
          <button class="save-btn" @click="saveSettings">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M5 13L9 17L19 7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            保存する
          </button>
        </div>
      </div>
    </div>
  </transition>
</template>

<script lang="ts">
import { defineComponent, reactive, ref, watch } from 'vue';
import { useStore } from 'vuex';

export default defineComponent({
  name: 'SettingsModal',
  
  props: {
    isOpen: {
      type: Boolean,
      default: false
    }
  },
  
  emits: ['close', 'save'],
  
  setup(props, { emit }) {
    const store = useStore();
    
    // 設定の初期値
    const settings = reactive({
      darkMode: false,
      fontSize: 'medium',
      notifications: true,
      notificationSound: true
    });
    
    // ストアから設定を取得
    const loadSettings = () => {
      const savedSettings = store.getters['settings/getSettings'];
      if (savedSettings) {
        settings.darkMode = savedSettings.darkMode;
        settings.fontSize = savedSettings.fontSize;
        settings.notifications = savedSettings.notifications;
        settings.notificationSound = savedSettings.notificationSound;
      }
    };
    
    // モーダルが開かれたとき設定を読み込む
    watch(() => props.isOpen, (newVal) => {
      if (newVal) {
        loadSettings();
      }
    });
    
    // モーダルを閉じる
    const closeModal = () => {
      emit('close');
    };
    
    // 設定を保存
    const saveSettings = () => {
      store.dispatch('settings/saveSettings', { ...settings });
      emit('save', { ...settings });
      closeModal();
    };
    
    return {
      settings,
      closeModal,
      saveSettings
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
  justify-content: center;
  align-items: center;
  z-index: 1000;
  backdrop-filter: blur(4px);
}

.modal-content {
  background-color: white;
  border-radius: 12px;
  width: 90%;
  max-width: 550px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
  box-sizing: border-box;
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

.settings-section {
  margin-bottom: 32px;
  width: 100%;
  box-sizing: border-box;
}

.settings-section:last-child {
  margin-bottom: 0;
}

.settings-section h4 {
  margin-top: 0;
  margin-bottom: 16px;
  font-size: 1.1rem;
  color: #333;
  font-weight: 600;
  border-bottom: 1px solid #eee;
  padding-bottom: 8px;
}

.setting-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding: 8px 0;
  width: 100%;
  box-sizing: border-box;
}

.setting-item:last-child {
  margin-bottom: 0;
}

.setting-item label {
  flex: 1;
  cursor: pointer;
}

.setting-label {
  display: block;
  font-weight: 600;
  color: #444;
  margin-bottom: 4px;
}

.setting-description {
  display: block;
  font-size: 0.85rem;
  color: #777;
}

/* トグルスイッチ */
.toggle-switch {
  position: relative;
  display: inline-block;
  width: 46px;
  height: 24px;
}

.toggle-switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.toggle-slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  border-radius: 34px;
  transition: 0.4s;
  border: 1px solid #b8b8b8;
}

.toggle-slider:before {
  position: absolute;
  content: "";
  height: 18px;
  width: 18px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  border-radius: 50%;
  transition: 0.4s;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
}

input:checked + .toggle-slider {
  background-color: #007bff;
  border-color: #0062cc;
}

input:checked + .toggle-slider:before {
  transform: translateX(22px);
}

.setting-item select {
  padding: 8px 12px;
  border: 2px solid #c8d0d9;
  border-radius: 8px;
  background-color: white;
  color: #333;
  font-weight: 500;
  width: 80px;
  font-size: 0.9rem;
  cursor: pointer;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='8' height='6' viewBox='0 0 8 6'%3E%3Cpath fill='%23333' d='M4 6L0 0h8z'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 12px center;
  background-size: 8px;
  padding-right: 30px;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.05);
  box-sizing: border-box;
}

.setting-item select:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.15);
}

.modal-footer {
  padding: 16px 24px;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.cancel-btn,
.save-btn {
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

.save-btn {
  background-color: #007bff;
  border: 1px solid #007bff;
  color: white;
}

.save-btn:hover {
  background-color: #0069d9;
  border-color: #0062cc;
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

:deep(.dark-mode) .settings-section h4 {
  color: #e0e0e0;
  border-bottom-color: #444;
}

:deep(.dark-mode) .setting-label {
  color: #ddd;
}

:deep(.dark-mode) .setting-description {
  color: #aaa;
}

:deep(.dark-mode) .setting-item select {
  background-color: #3a3a3a;
  border-color: #555;
  border-width: 2px;
  color: #f5f5f5;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='8' height='6' viewBox='0 0 8 6'%3E%3Cpath fill='%23ddd' d='M4 6L0 0h8z'/%3E%3C/svg%3E");
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.2);
}

:deep(.dark-mode) .setting-item select:focus {
  border-color: #4d94ff;
  box-shadow: 0 0 0 3px rgba(77, 148, 255, 0.15);
}

:deep(.dark-mode) .toggle-slider {
  background-color: #555;
  border-color: #444;
}

:deep(.dark-mode) .toggle-slider:before {
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.4);
}

:deep(.dark-mode) input:checked + .toggle-slider {
  background-color: #0d6efd;
  border-color: #0a58ca;
}

:deep(.dark-mode) .modal-footer {
  border-top-color: #444;
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

:deep(.dark-mode) .save-btn {
  background-color: #0d6efd;
  border-color: #0d6efd;
}

:deep(.dark-mode) .save-btn:hover {
  background-color: #0b5ed7;
  border-color: #0a58ca;
}

@media (max-width: 576px) {
  .modal-content {
    width: 95%;
    max-width: none;
    border-radius: 10px;
  }
  
  .settings-section {
    margin-bottom: 24px;
  }
  
  .setting-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  
  .setting-item label {
    margin-bottom: 8px;
  }
  
  .toggle-switch {
    align-self: flex-start;
  }
  
  .setting-item select {
    width: 100%;
  }
  
  .modal-footer {
    flex-direction: column-reverse;
  }
  
  .cancel-btn, 
  .save-btn {
    width: 100%;
    justify-content: center;
  }
}
</style> 
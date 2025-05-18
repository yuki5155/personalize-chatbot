<template>
  <div v-if="isOpen" class="modal-overlay" @click="closeModal">
    <div class="modal-container" @click.stop>
      <div class="modal-header">
        <h2>チャット設定</h2>
        <button class="close-button" @click="closeModal">&times;</button>
      </div>
      <div class="modal-body">
        <div class="settings-section">
          <h3>表示設定</h3>
          <div class="setting-item">
            <label for="darkMode">ダークモード</label>
            <input 
              type="checkbox" 
              id="darkMode" 
              v-model="settings.darkMode"
            />
          </div>
          <div class="setting-item">
            <label for="fontSize">文字サイズ</label>
            <select id="fontSize" v-model="settings.fontSize">
              <option value="small">小</option>
              <option value="medium">中</option>
              <option value="large">大</option>
            </select>
          </div>
        </div>
        
        <div class="settings-section">
          <h3>通知設定</h3>
          <div class="setting-item">
            <label for="notifications">通知を有効にする</label>
            <input 
              type="checkbox" 
              id="notifications" 
              v-model="settings.notifications"
            />
          </div>
          <div class="setting-item">
            <label for="notificationSound">通知音</label>
            <input 
              type="checkbox" 
              id="notificationSound" 
              v-model="settings.notificationSound"
            />
          </div>
        </div>
      </div>
      <div class="modal-footer">
        <button class="cancel-button" @click="closeModal">キャンセル</button>
        <button class="save-button" @click="saveSettings">保存</button>
      </div>
    </div>
  </div>
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
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-container {
  background-color: white;
  border-radius: 8px;
  width: 500px;
  max-width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border-bottom: 1px solid #e0e0e0;
}

.modal-header h2 {
  margin: 0;
  font-size: 1.2rem;
  color: #333;
}

.close-button {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #666;
}

.modal-body {
  padding: 1.5rem;
}

.settings-section {
  margin-bottom: 1.5rem;
}

.settings-section h3 {
  margin-top: 0;
  margin-bottom: 1rem;
  font-size: 1.1rem;
  color: #444;
  border-bottom: 1px solid #eee;
  padding-bottom: 0.5rem;
}

.setting-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding: 0.5rem 0;
}

.setting-item label {
  flex: 1;
  font-weight: 500;
  color: #555;
}

.setting-item input[type="checkbox"] {
  width: 18px;
  height: 18px;
}

.setting-item select {
  padding: 0.3rem 0.3rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: white;
  color: #333;
  font-weight: 500;
  width: 60px;
  font-size: 0.85rem;
  cursor: pointer;
}

.setting-item select:focus {
  outline: 1px solid #42b983;
  border-color: #42b983;
}

.setting-item select option {
  padding: 0.3rem;
  background-color: white;
  color: #333;
  font-size: 0.9rem;
}

.setting-item select option:checked {
  background-color: #eaf7f1;
  color: #42b983;
  font-weight: bold;
}

.modal-footer {
  padding: 1rem;
  border-top: 1px solid #e0e0e0;
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}

.cancel-button {
  background-color: #f5f5f5;
  color: #333;
  border: 1px solid #ddd;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
}

.save-button {
  background-color: #42b983;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
}

.save-button:hover {
  background-color: #3aa876;
}
</style> 
import { Module, ActionContext } from 'vuex';
import { RootState } from '../types';

export interface SettingsState {
  darkMode: boolean;
  fontSize: string;
  notifications: boolean;
  notificationSound: boolean;
}

const settingsModule: Module<SettingsState, RootState> = {
  namespaced: true,
  
  state: () => ({
    darkMode: false,
    fontSize: 'medium',
    notifications: true,
    notificationSound: true
  }),
  
  mutations: {
    setSettings(state: SettingsState, settings: Partial<SettingsState>) {
      Object.assign(state, settings);
    }
  },
  
  actions: {
    loadSettings({ commit }: ActionContext<SettingsState, RootState>) {
      const settingsStr = localStorage.getItem('chatSettings');
      if (settingsStr) {
        try {
          const settings = JSON.parse(settingsStr);
          commit('setSettings', settings);
        } catch (error) {
          console.error('設定の読み込みに失敗しました:', error);
        }
      }
    },
    
    saveSettings({ commit }: ActionContext<SettingsState, RootState>, settings: Partial<SettingsState>) {
      commit('setSettings', settings);
      
      // ローカルストレージに保存
      localStorage.setItem('chatSettings', JSON.stringify(settings));
      
      return settings;
    }
  },
  
  getters: {
    getSettings: (state: SettingsState) => state
  }
};

export default settingsModule; 
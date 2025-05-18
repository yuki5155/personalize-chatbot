import { createStore } from 'vuex';
import { RootState } from './types';
import chatModule from './modules/chat';
import authModule from './modules/auth';
import settingsModule from './modules/settings';

export default createStore<RootState>({
  state: {
    // ルートの状態
  },
  modules: {
    chat: chatModule,
    auth: authModule,
    settings: settingsModule
  }
}); 
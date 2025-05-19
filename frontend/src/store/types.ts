import { AuthState } from './modules/auth';
import { SettingsState } from './modules/settings';
import { ChatState } from './modules/chat';

export interface RootState {
  // ルートの状態型定義
  auth?: AuthState;
  settings?: SettingsState;
  chat?: ChatState;
} 
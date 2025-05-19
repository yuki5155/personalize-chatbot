import { Module } from 'vuex';
import { RootState } from '../../types';
import { chatService } from '../../../api/services';

// メッセージの型定義
export interface Message {
  id: number;
  text: string;
  sender: 'user' | 'assistant';
  timestamp: number;
}

// スレッドの型定義
export interface Thread {
  id: number;
  title: string;
  messages: Message[];
  createdAt: number;
  updatedAt: number;
  isActive: boolean;
}

// チャットの状態の型定義
export interface ChatState {
  threads: Thread[];
  currentThreadId: number | null;
  loading: boolean;
  error: string | null;
}

// ActionContextの型定義
type Context = {
  commit: (type: string, payload?: any) => void;
  dispatch: (type: string, payload?: any) => Promise<any>;
  state: ChatState;
  rootState: RootState;
};

const chatModule: Module<ChatState, RootState> = {
  namespaced: true,
  
  state: {
    threads: [],
    currentThreadId: null,
    loading: false,
    error: null
  },
  
  getters: {
    allThreads: (state: ChatState) => state.threads,
    activeThreads: (state: ChatState) => state.threads.filter(thread => thread.isActive),
    currentThread: (state: ChatState) => {
      if (state.currentThreadId === null) return null;
      return state.threads.find(thread => thread.id === state.currentThreadId) || null;
    },
    totalMessageCount: (state: ChatState) => {
      return state.threads.reduce((total, thread) => total + thread.messages.length, 0);
    },
    totalThreadCount: (state: ChatState) => state.threads.length,
    activeThreadCount: (state: ChatState) => state.threads.filter(thread => thread.isActive).length,
    isLoading: (state: ChatState) => state.loading,
    error: (state: ChatState) => state.error
  },
  
  mutations: {
    setLoading(state: ChatState, loading: boolean) {
      state.loading = loading;
    },
    
    setError(state: ChatState, error: string | null) {
      state.error = error;
    },
    
    setThreads(state: ChatState, threads: Thread[]) {
      state.threads = threads;
    },
    
    setCurrentThreadId(state: ChatState, threadId: number | null) {
      state.currentThreadId = threadId;
    },
    
    addThread(state: ChatState, thread: Thread) {
      state.threads.push(thread);
      state.currentThreadId = thread.id;
    },
    
    addMessage(state: ChatState, { threadId, message }: { threadId: number, message: Message }) {
      const thread = state.threads.find(t => t.id === threadId);
      
      if (thread) {
        thread.messages.push(message);
        thread.updatedAt = Date.now();
      }
    },
    
    toggleThreadActive(state: ChatState, threadId: number) {
      const thread = state.threads.find(t => t.id === threadId);
      if (thread) {
        thread.isActive = !thread.isActive;
      }
    }
  },
  
  actions: {
    // スレッドをAPIからロード
    async loadThreads({ commit, state }: Context) {
      commit('setLoading', true);
      commit('setError', null);
      
      try {
        const threads = await chatService.getThreads();
        commit('setThreads', threads);
        
        // 最初のスレッドをカレントに設定
        if (threads.length > 0 && !state.currentThreadId) {
          commit('setCurrentThreadId', threads[0].id);
        }
      } catch (error) {
        console.error('Error loading threads:', error);
        commit('setError', 'スレッドの読み込みに失敗しました');
        commit('setThreads', []);
      } finally {
        commit('setLoading', false);
      }
    },
    
    // 新しいスレッドを作成
    async createThread({ commit, dispatch }: Context, { title, firstMessage }: { title: string, firstMessage: string }) {
      commit('setLoading', true);
      commit('setError', null);
      
      try {
        const newThread = await chatService.createThread(title, firstMessage);
        commit('addThread', newThread);
      } catch (error) {
        console.error('Error creating thread:', error);
        commit('setError', 'スレッドの作成に失敗しました');
      } finally {
        commit('setLoading', false);
      }
    },
    
    // メッセージを送信（ユーザーから）
    async sendMessage({ commit, state }: Context, text: string) {
      if (!state.currentThreadId) return;
      
      try {
        // ユーザーメッセージを送信
        const userMessage = await chatService.sendMessage(state.currentThreadId, text);
        commit('addMessage', {
          threadId: state.currentThreadId,
          message: userMessage
        });
        
        // ボットの応答をシミュレート
        setTimeout(async () => {
          // 実際のAPIでは、ここでボットの応答を取得するエンドポイントを呼び出す
          const botMessage: Message = {
            id: Math.floor(Math.random() * 10000),
            text: `「${text}」に対する応答です。これはシミュレートされたボットの返信です。`,
            sender: 'assistant',
            timestamp: Date.now()
          };
          
          commit('addMessage', {
            threadId: state.currentThreadId,
            message: botMessage
          });
        }, 1000);
      } catch (error) {
        console.error('Error sending message:', error);
        commit('setError', 'メッセージの送信に失敗しました');
      }
    },
    
    // スレッドの有効/無効を切り替え
    toggleThread({ commit }: Context, threadId: number) {
      commit('toggleThreadActive', threadId);
    },
    
    // 現在のスレッドを変更
    setCurrentThread({ commit }: Context, threadId: number | null) {
      commit('setCurrentThreadId', threadId);
    }
  }
};

export default chatModule; 
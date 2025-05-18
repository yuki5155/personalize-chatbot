import { Module } from 'vuex';
import { RootState } from '../../types';

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
}

const chatModule: Module<ChatState, RootState> = {
  namespaced: true,
  
  state: {
    threads: [],
    currentThreadId: null,
    loading: false
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
    activeThreadCount: (state: ChatState) => state.threads.filter(thread => thread.isActive).length
  },
  
  mutations: {
    setLoading(state: ChatState, loading: boolean) {
      state.loading = loading;
    },
    
    setThreads(state: ChatState, threads: Thread[]) {
      state.threads = threads;
    },
    
    setCurrentThreadId(state: ChatState, threadId: number | null) {
      state.currentThreadId = threadId;
    },
    
    addThread(state: ChatState, title: string) {
      const newId = state.threads.length > 0 
        ? Math.max(...state.threads.map(t => t.id)) + 1 
        : 1;
      
      const now = Date.now();
      
      const newThread: Thread = {
        id: newId,
        title: title || `スレッド ${newId}`,
        messages: [],
        createdAt: now,
        updatedAt: now,
        isActive: true
      };
      
      state.threads.push(newThread);
      state.currentThreadId = newId;
    },
    
    addMessage(state: ChatState, { threadId, text, sender }: { threadId: number, text: string, sender: 'user' | 'assistant' }) {
      const thread = state.threads.find(t => t.id === threadId);
      
      if (thread) {
        const newId = thread.messages.length > 0 
          ? Math.max(...thread.messages.map(m => m.id)) + 1 
          : 1;
        
        thread.messages.push({
          id: newId,
          text,
          sender,
          timestamp: Date.now()
        });
        
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
    // スレッドをロード
    loadThreads({ commit }) {
      commit('setLoading', true);
      
      // localStorage から読み込み（実際のアプリではAPIからロードする場合も）
      setTimeout(() => {
        try {
          const savedThreads = localStorage.getItem('chatThreads');
          if (savedThreads) {
            commit('setThreads', JSON.parse(savedThreads));
          } else {
            // 初期スレッド
            commit('setThreads', []);
          }
        } catch (error) {
          console.error('Error loading threads:', error);
          commit('setThreads', []);
        } finally {
          commit('setLoading', false);
        }
      }, 500);
    },
    
    // スレッドを保存
    saveThreads({ state }) {
      localStorage.setItem('chatThreads', JSON.stringify(state.threads));
    },
    
    // 新しいスレッドを作成
    createThread({ commit, dispatch }, title: string) {
      commit('setLoading', true);
      
      setTimeout(() => {
        commit('addThread', title);
        dispatch('saveThreads');
        commit('setLoading', false);
      }, 300);
    },
    
    // メッセージを送信（ユーザーから）
    sendMessage({ commit, dispatch, state }, text: string) {
      if (!state.currentThreadId) return;
      
      commit('addMessage', {
        threadId: state.currentThreadId,
        text,
        sender: 'user'
      });
      
      // ボットの応答をシミュレート
      setTimeout(() => {
        commit('addMessage', {
          threadId: state.currentThreadId,
          text: `「${text}」に対する応答です。これはシミュレートされたボットの返信です。`,
          sender: 'assistant'
        });
        
        dispatch('saveThreads');
      }, 1000);
    },
    
    // スレッドの有効/無効を切り替え
    toggleThread({ commit, dispatch }, threadId: number) {
      commit('toggleThreadActive', threadId);
      dispatch('saveThreads');
    },
    
    // 現在のスレッドを変更
    setCurrentThread({ commit }, threadId: number | null) {
      commit('setCurrentThreadId', threadId);
    }
  }
};

export default chatModule; 
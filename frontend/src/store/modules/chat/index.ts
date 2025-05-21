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
  isTyping: boolean; // ボットが入力中かどうか
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
    error: null,
    isTyping: false
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
    isTyping: (state: ChatState) => state.isTyping,
    error: (state: ChatState) => state.error
  },
  
  mutations: {
    setLoading(state: ChatState, loading: boolean) {
      state.loading = loading;
    },
    
    setTyping(state: ChatState, isTyping: boolean) {
      state.isTyping = isTyping;
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
    
    updateMessageText(state: ChatState, { threadId, messageId, text }: { threadId: number, messageId: number, text: string }) {
      const thread = state.threads.find(t => t.id === threadId);
      
      if (thread) {
        const message = thread.messages.find(m => m.id === messageId);
        if (message) {
          message.text = text;
        }
      }
    },
    
    setThreadMessages(state: ChatState, { threadId, messages }: { threadId: number, messages: Message[] }) {
      const thread = state.threads.find(t => t.id === threadId);
      
      if (thread) {
        thread.messages = messages;
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
    
    // スレッドのメッセージをロード
    async loadMessages({ commit, state }: Context, threadId: number) {
      if (!threadId) return;
      
      commit('setLoading', true);
      commit('setError', null);
      
      try {
        const messages = await chatService.getMessages(threadId);
        commit('setThreadMessages', { threadId, messages });
      } catch (error) {
        console.error(`Error loading messages for thread ${threadId}:`, error);
        commit('setError', 'メッセージの読み込みに失敗しました');
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
        
        // スレッドが作成されたらメッセージも読み込む
        if (newThread.id) {
          await dispatch('loadMessages', newThread.id);
        }
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
        
        // ボットの応答を取得中の状態にする
        commit('setTyping', true);
        
        // アシスタントの応答を取得 (実際のシステムではここはWebSocket等のリアルタイム通信になる可能性あり)
        // 今回はモックAPIのため、シミュレーションとして一定時間後に応答
        setTimeout(async () => {
          try {
            const botMessage = await chatService.sendAssistantMessage(state.currentThreadId as number, 
              `「${text}」について理解しました。どのようにお手伝いできますか？`);
            
            commit('addMessage', {
              threadId: state.currentThreadId as number,
              message: botMessage
            });
          } catch (error) {
            console.error('Error getting bot response:', error);
            commit('setError', 'ボットの応答を取得できませんでした');
          } finally {
            commit('setTyping', false);
          }
        }, 1500);
      } catch (error) {
        console.error('Error sending message:', error);
        commit('setError', 'メッセージの送信に失敗しました');
        commit('setTyping', false);
      }
    },
    
    // メッセージを送信（ユーザーから）- ストリーミングレスポンス版
    async sendMessageWithStreamingResponse({ commit, state }: Context, text: string) {
      if (!state.currentThreadId) return;
      
      try {
        console.log('ストリーミングレスポンスアクション開始:', text);
        
        // ユーザーメッセージを送信
        const userMessage = await chatService.sendMessage(state.currentThreadId, text);
        console.log('ユーザーメッセージ送信完了:', userMessage);
        
        commit('addMessage', {
          threadId: state.currentThreadId,
          message: userMessage
        });
        
        // ボットの応答を取得中の状態にする
        commit('setTyping', true);
        
        // メッセージの空のシェルを作成
        const initialBotMessage = {
          id: userMessage.id + 1,  // 一時的なID (実際にはサーバーからの応答で上書きされる)
          text: '',
          sender: 'assistant' as 'assistant',
          timestamp: Date.now()
        };
        
        console.log('初期ボットメッセージを作成:', initialBotMessage);
        
        commit('addMessage', {
          threadId: state.currentThreadId,
          message: initialBotMessage
        });
        
        // ストリーミングレスポンスを開始
        await chatService.sendAssistantMessageStream(
          state.currentThreadId,
          `「${text}」について理解しました。どのようにお手伝いできますか？`,
          (progressText) => {
            console.log('ストリーミング進捗:', progressText);
            // 進捗に応じてメッセージを更新
            commit('updateMessageText', {
              threadId: state.currentThreadId,
              messageId: initialBotMessage.id,
              text: progressText
            });
          }
        );
        
        console.log('ストリーミングレスポンス完了');
      } catch (error) {
        console.error('Error sending message with streaming response:', error);
        commit('setError', 'メッセージの送信に失敗しました');
      } finally {
        commit('setTyping', false);
      }
    },
    
    // スレッドの有効/無効を切り替え
    toggleThread({ commit }: Context, threadId: number) {
      commit('toggleThreadActive', threadId);
    },
    
    // 現在のスレッドを変更
    async setCurrentThread({ commit, dispatch }: Context, threadId: number | null) {
      commit('setCurrentThreadId', threadId);
      
      // スレッドが選択されたらメッセージを読み込む
      if (threadId !== null) {
        await dispatch('loadMessages', threadId);
      }
    }
  }
};

export default chatModule; 
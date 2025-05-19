import apiClient from '../index';
import { Thread, Message } from '../../store/modules/chat';

// スレッド関連のAPI呼び出し
const chatService = {
  // スレッド一覧の取得
  getThreads: async (): Promise<Thread[]> => {
    try {
      const response = await apiClient.get('/threads');
      return response.data;
    } catch (error) {
      console.error('スレッド一覧の取得に失敗しました:', error);
      throw error;
    }
  },

  // 特定のスレッドの取得
  getThread: async (threadId: number): Promise<Thread> => {
    try {
      const response = await apiClient.get(`/threads/${threadId}`);
      return response.data;
    } catch (error) {
      console.error(`スレッド ${threadId} の取得に失敗しました:`, error);
      throw error;
    }
  },

  // スレッドのメッセージ一覧を取得
  getMessages: async (threadId: number): Promise<Message[]> => {
    try {
      const response = await apiClient.get(`/messages/${threadId}`);
      return response.data;
    } catch (error) {
      console.error(`スレッド ${threadId} のメッセージ取得に失敗しました:`, error);
      throw error;
    }
  },

  // 新しいメッセージの送信
  sendMessage: async (threadId: number, text: string): Promise<Message> => {
    try {
      const response = await apiClient.post(`/messages/${threadId}`, { text });
      return response.data;
    } catch (error) {
      console.error('メッセージの送信に失敗しました:', error);
      throw error;
    }
  },

  // アシスタントからのメッセージ送信 (主にデバッグ・テスト用)
  sendAssistantMessage: async (threadId: number, text: string): Promise<Message> => {
    try {
      const response = await apiClient.post(`/messages/${threadId}/assistant`, { text });
      return response.data;
    } catch (error) {
      console.error('アシスタントメッセージの送信に失敗しました:', error);
      throw error;
    }
  },

  // 新しいスレッドの作成
  createThread: async (title: string, first_message: string): Promise<Thread> => {
    try {
      const response = await apiClient.post('/threads', {
        title,
        first_message
      });
      return response.data;
    } catch (error) {
      console.error('スレッドの作成に失敗しました:', error);
      throw error;
    }
  }
};

export default chatService; 
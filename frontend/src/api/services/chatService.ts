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

  // 新しいメッセージの送信 (実際のAPIでは別途エンドポイントがあるはずですが、今回のモックAPIでは未実装)
  // 実際のエンドポイントに合わせて適宜変更してください
  sendMessage: async (threadId: number, text: string): Promise<Message> => {
    try {
      // 実際のAPIエンドポイントがある場合はここでPOSTリクエストを送信
      // ダミーレスポンスを返す（モックAPI対応）
      const dummyResponse = {
        id: Math.floor(Math.random() * 10000),
        text: text,
        sender: 'user',
        timestamp: Date.now()
      } as Message;

      return dummyResponse;
    } catch (error) {
      console.error('メッセージの送信に失敗しました:', error);
      throw error;
    }
  },

  // 新しいスレッドの作成 (実際のAPIでは別途エンドポイントがあるはずですが、今回のモックAPIでは未実装)
  // 実際のエンドポイントに合わせて適宜変更してください
  createThread: async (title: string): Promise<Thread> => {
    try {
      // 実際のAPIエンドポイントがある場合はここでPOSTリクエストを送信
      // ダミーレスポンスを返す（モックAPI対応）
      const dummyResponse = {
        id: Math.floor(Math.random() * 10000),
        title,
        messages: [],
        createdAt: Date.now(),
        updatedAt: Date.now(),
        isActive: true
      } as Thread;

      return dummyResponse;
    } catch (error) {
      console.error('スレッドの作成に失敗しました:', error);
      throw error;
    }
  }
};

export default chatService; 
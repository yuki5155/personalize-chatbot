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

  // アシスタントからのメッセージ送信 (ストリーミング)
  sendAssistantMessageStream: async (
    threadId: number, 
    text: string,
    onProgress: (text: string) => void
  ): Promise<void> => {
    try {
      console.log(`ストリーミングリクエスト開始: threadId=${threadId}, text="${text}"`);
      
      // Viteのプロキシ設定を使用して相対パスで通信
      const url = `/messages/${threadId}/assistant/stream`;
      
      console.log('ストリーミングURL:', url);
      
      // Response typeをblobに設定して生のデータを受け取る
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text }),
        credentials: 'include', // クッキーを送信するために必要
      });

      console.log('ストリーミングレスポンス受信:', response.status, response.statusText);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}, statusText: ${response.statusText}`);
      }

      // レスポンスをストリームとして読み込む
      const reader = response.body?.getReader();
      if (!reader) {
        throw new Error('Response body is null');
      }

      const decoder = new TextDecoder();
      let receivedText = '';

      // ストリームからデータを読み込み続ける
      while (true) {
        const { done, value } = await reader.read();
        
        if (done) {
          console.log('ストリーミング完了:', receivedText);
          break;
        }
        
        // バイナリデータをテキストにデコード
        const chunk = decoder.decode(value, { stream: true });
        console.log('チャンク受信:', chunk);
        receivedText += chunk;
        
        // 進捗コールバックを呼び出す
        onProgress(receivedText);
      }
    } catch (error) {
      console.error('ストリーミングメッセージの送信に失敗しました:', error);
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
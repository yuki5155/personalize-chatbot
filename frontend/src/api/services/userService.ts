import apiClient from '../index';

/**
 * ユーザーに関連するAPI呼び出しを行うサービス
 */
const userService = {
  /**
   * ユーザークッキーを設定するAPI呼び出し
   * @returns {Promise<any>} APIレスポンス
   */
  setUserCookie: async (): Promise<any> => {
    try {
      const response = await apiClient.get('/users/set-cookie');
      return response.data;
    } catch (error) {
      console.error('ユーザークッキー設定エラー:', error);
      throw error;
    }
  },

  /**
   * 現在のユーザー情報を取得するAPI呼び出し
   * @returns {Promise<any>} ユーザー情報
   */
  getCurrentUser: async (): Promise<any> => {
    try {
      const response = await apiClient.get('/users/me');
      return response.data;
    } catch (error) {
      console.error('ユーザー情報取得エラー:', error);
      throw error;
    }
  }
};

export default userService; 
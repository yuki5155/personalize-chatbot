import axios from 'axios';

// API基本設定
const apiClient = axios.create({
  // ベースURLなしで相対パスを使用（プロキシ設定に合わせる）
  baseURL: '/', 
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
  withCredentials: true, // クッキーを送受信するために必要
});

// レスポンスインターセプター
apiClient.interceptors.response.use(
  response => response,
  error => {
    console.error('API呼び出しエラー:', error);
    return Promise.reject(error);
  }
);

export default apiClient; 
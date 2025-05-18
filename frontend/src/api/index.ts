import axios from 'axios';

// API基本設定
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
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
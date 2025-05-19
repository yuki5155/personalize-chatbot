import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      // すべてのAPIリクエストを処理する単一のプロキシルール
      '/users': {
        target: 'http://host.docker.internal:8001', // Dockerコンテナからホストマシンにアクセス
        changeOrigin: true,
        secure: false,
        ws: true
      }
    }
  }
}) 
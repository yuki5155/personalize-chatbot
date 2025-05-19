import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      // APIリクエストを処理するプロキシルール
      '/api': {
        target: 'http://host.docker.internal:8001', // Dockerコンテナからホストマシンにアクセス
        changeOrigin: true,
        secure: false,
        ws: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      },
      '/users': {
        target: 'http://host.docker.internal:8001', // Dockerコンテナからホストマシンにアクセス
        changeOrigin: true,
        secure: false,
        ws: true
      },
      '/threads': {
        target: 'http://host.docker.internal:8001', // FastAPIサーバー
        changeOrigin: true,
        secure: false,
        ws: true
      },
      '/messages': {
        target: 'http://host.docker.internal:8001', // FastAPIサーバー
        changeOrigin: true,
        secure: false,
        ws: true
      }
    }
  }
}) 
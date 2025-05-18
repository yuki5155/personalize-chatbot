<template>
  <div class="home">
    <h1>Chatbot App</h1>
    <div class="content">
      <div class="features">
        <div class="feature">
          <h2>📝 スレッド機能</h2>
          <p>複数の会話スレッドを作成し、整理できます。</p>
        </div>
        <div class="feature">
          <h2>💬 自動応答</h2>
          <p>あなたのメッセージに自動で応答します。</p>
        </div>
        <div class="feature">
          <h2>📊 統計情報</h2>
          <p>マイページでスレッド数や会話数を確認できます。</p>
        </div>
      </div>
      <div class="actions">
        <router-link to="/chat" class="button start-chat">
          チャットを始める
        </router-link>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'HomePage'
});
</script>

<style scoped>
.home {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.content {
  max-width: 800px;
  text-align: center;
}

.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin: 3rem 0;
}

.feature {
  padding: 1.5rem;
  background-color: rgba(66, 185, 131, 0.1);
  border-radius: 8px;
  transition: transform 0.3s ease;
}

.feature:hover {
  transform: translateY(-5px);
}

h1 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
  color: #42b983;
}

h2 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: #42b983;
}

.actions {
  margin-top: 2rem;
}

.button {
  display: inline-block;
  padding: 0.8rem 1.5rem;
  border-radius: 4px;
  font-weight: bold;
  text-decoration: none;
  transition: background-color 0.3s ease;
}

.start-chat {
  background-color: #42b983;
  color: white;
}

.start-chat:hover {
  background-color: #3da776;
}
</style> 
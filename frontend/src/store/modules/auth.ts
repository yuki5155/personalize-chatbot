import { Module, ActionContext } from 'vuex';
import { RootState } from '../types';

export interface AuthState {
  isAuthenticated: boolean;
  user: {
    username: string;
  } | null;
}

const authModule: Module<AuthState, RootState> = {
  namespaced: true,
  
  state: () => ({
    isAuthenticated: false,
    user: null
  }),
  
  mutations: {
    setAuth(state: AuthState, isAuthenticated: boolean) {
      state.isAuthenticated = isAuthenticated;
    },
    setUser(state: AuthState, user: { username: string } | null) {
      state.user = user;
    }
  },
  
  actions: {
    login({ commit }: ActionContext<AuthState, RootState>, username: string) {
      // 実際のアプリでは、ここで認証APIを呼び出します
      commit('setAuth', true);
      commit('setUser', { username });
      
      // ローカルストレージに保存（実際のアプリではトークンを保存）
      localStorage.setItem('user', JSON.stringify({ username }));
    },
    
    logout({ commit }: ActionContext<AuthState, RootState>) {
      commit('setAuth', false);
      commit('setUser', null);
      
      // ローカルストレージから削除
      localStorage.removeItem('user');
    },
    
    checkAuth({ commit }: ActionContext<AuthState, RootState>) {
      // ページ読み込み時に認証状態を確認
      const userStr = localStorage.getItem('user');
      if (userStr) {
        const user = JSON.parse(userStr);
        commit('setAuth', true);
        commit('setUser', user);
      }
    }
  },
  
  getters: {
    isAuthenticated: (state: AuthState) => state.isAuthenticated,
    currentUser: (state: AuthState) => state.user
  }
};

export default authModule; 
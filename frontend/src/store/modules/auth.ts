import { Module, ActionContext } from 'vuex';
import { RootState } from '../types';
import { userService } from '../../api/services';

export interface AuthState {
  isAuthenticated: boolean;
  user: any | null;
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
    setUser(state: AuthState, user: any | null) {
      state.user = user;
    }
  },
  
  actions: {
    // ログイン処理
    async login({ commit }: ActionContext<AuthState, RootState>) {
      try {
        // バックエンドのset-cookieエンドポイントを呼び出す
        await userService.setUserCookie();
        
        // ユーザー情報を取得
        const userData = await userService.getCurrentUser();
        
        commit('setAuth', true);
        commit('setUser', userData);
        
        return userData;
      } catch (error) {
        console.error('ログインエラー:', error);
        throw error;
      }
    },
    
    // ログアウト処理
    logout({ commit }: ActionContext<AuthState, RootState>) {
      // 実際のアプリではここでログアウトAPIを呼び出す
      commit('setAuth', false);
      commit('setUser', null);
    },
    
    // 認証状態チェック
    async checkAuth({ commit }: ActionContext<AuthState, RootState>) {
      try {
        // バックエンドからユーザー情報を取得
        const userData = await userService.getCurrentUser();
        commit('setAuth', true);
        commit('setUser', userData);
        return userData;
      } catch (error) {
        // エラーの場合は認証されていない
        commit('setAuth', false);
        commit('setUser', null);
        return null;
      }
    }
  },
  
  getters: {
    isAuthenticated: (state: AuthState) => state.isAuthenticated,
    currentUser: (state: AuthState) => state.user
  }
};

export default authModule; 
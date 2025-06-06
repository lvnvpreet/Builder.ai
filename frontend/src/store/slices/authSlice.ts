import { StateCreator } from 'zustand';

export interface User {
  id: string;
  email: string;
  name?: string;
}

export interface AuthState {
  user: User | null;
  token: string | null;
  isLoading: boolean;
  error: string | null;
}

export interface AuthSlice {
  auth: AuthState;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  signup: (email: string, password: string, name?: string) => Promise<void>;
  setAuthLoading: (isLoading: boolean) => void;
  setAuthError: (error: string | null) => void;
}

export const createAuthSlice: StateCreator<
  AuthSlice,
  [],
  [],
  AuthSlice
> = (set) => ({
  auth: {
    user: null,
    token: null,
    isLoading: false,
    error: null
  },
  
  login: async (email: string, password: string) => {
    set((state) => ({ 
      auth: { 
        ...state.auth, 
        isLoading: true,
        error: null 
      } 
    }));
    
    try {
      // For now, we'll use a mock login
      // In a real app, you'd make an API call here
      const response = await new Promise<{user: User, token: string}>((resolve) => {
        setTimeout(() => {
          resolve({
            user: { 
              id: '1', 
              email,
              name: 'Demo User'
            },
            token: 'mock-token-12345'
          });
        }, 1000);
      });
      
      set((state) => ({
        auth: {
          ...state.auth,
          user: response.user,
          token: response.token,
          isLoading: false
        }
      }));
    } catch (error: any) {
      set((state) => ({ 
        auth: { 
          ...state.auth, 
          isLoading: false,
          error: error?.message || 'Login failed' 
        } 
      }));
    }
  },
  
  logout: () => {
    set((state) => ({
      auth: {
        ...state.auth,
        user: null,
        token: null
      }
    }));
  },
  
  signup: async (email: string, password: string, name?: string) => {
    set((state) => ({ 
      auth: { 
        ...state.auth, 
        isLoading: true,
        error: null 
      } 
    }));
    
    try {
      // Mock signup
      const response = await new Promise<{user: User, token: string}>((resolve) => {
        setTimeout(() => {
          resolve({
            user: { 
              id: '1', 
              email,
              name: name || 'New User'
            },
            token: 'mock-token-12345'
          });
        }, 1000);
      });
      
      set((state) => ({
        auth: {
          ...state.auth,
          user: response.user,
          token: response.token,
          isLoading: false
        }
      }));
    } catch (error: any) {
      set((state) => ({ 
        auth: { 
          ...state.auth, 
          isLoading: false,
          error: error?.message || 'Signup failed' 
        } 
      }));
    }
  },
  
  setAuthLoading: (isLoading: boolean) => {
    set((state) => ({
      auth: { ...state.auth, isLoading }
    }));
  },
  
  setAuthError: (error: string | null) => {
    set((state) => ({
      auth: { ...state.auth, error }
    }));
  }
});

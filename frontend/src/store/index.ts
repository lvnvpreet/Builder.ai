import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';
import { createAuthSlice, AuthSlice } from './slices/authSlice';
import { createGenerationSlice, GenerationSlice } from './slices/generationSlice';
import { createUISlice, UISlice } from './slices/uiSlice';
import { createWebsiteSlice, WebsiteSlice } from './slices/websiteSlice';

export type AppState = AuthSlice & GenerationSlice & UISlice & WebsiteSlice;

export const useAppStore = create<AppState>()(
  devtools(
    persist(
      (set, get, api) => ({
        ...createAuthSlice(set, get, api),
        ...createGenerationSlice(set, get, api),
        ...createUISlice(set, get, api),
        ...createWebsiteSlice(set, get, api),
      }),
      {
        name: 'ai-website-builder',
        partialize: (state) => ({
          // Only persist auth state and completed generations
          auth: state.auth,
          generationHistory: state.generationHistory,
        }),
      }
    ),
    { name: 'AI Website Builder Store' }
  )
);

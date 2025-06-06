import { StateCreator } from 'zustand';

export interface UIState {
  isSidebarOpen: boolean;
  activeTab: string;
  theme: 'light' | 'dark' | 'system';
}

export interface UISlice {
  ui: UIState;
  toggleSidebar: () => void;
  setSidebarOpen: (isOpen: boolean) => void;
  setActiveTab: (tab: string) => void;
  setTheme: (theme: 'light' | 'dark' | 'system') => void;
}

export const createUISlice: StateCreator<
  UISlice,
  [],
  [],
  UISlice
> = (set) => ({
  ui: {
    isSidebarOpen: true,
    activeTab: 'dashboard',
    theme: 'light',
  },
  
  toggleSidebar: () => {
    set((state) => ({
      ui: {
        ...state.ui,
        isSidebarOpen: !state.ui.isSidebarOpen
      }
    }));
  },
  
  setSidebarOpen: (isOpen: boolean) => {
    set((state) => ({
      ui: {
        ...state.ui,
        isSidebarOpen: isOpen
      }
    }));
  },
  
  setActiveTab: (tab: string) => {
    set((state) => ({
      ui: {
        ...state.ui,
        activeTab: tab
      }
    }));
  },
  
  setTheme: (theme: 'light' | 'dark' | 'system') => {
    set((state) => ({
      ui: {
        ...state.ui,
        theme
      }
    }));
  }
});

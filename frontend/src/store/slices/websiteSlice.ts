import { StateCreator } from 'zustand';
import { GenerationResult, WebsitePage } from '@/types/generation';

export interface WebsiteState {
  currentWebsite: GenerationResult | null;
  savedWebsites: GenerationResult[];
  currentPreviewPage: string | null;
}

export interface WebsiteSlice {
  website: WebsiteState;
  setCurrentWebsite: (website: GenerationResult | null) => void;
  saveWebsite: (website: GenerationResult) => void;
  deleteWebsite: (websiteId: string) => void;
  setCurrentPreviewPage: (pageId: string | null) => void;
}

export const createWebsiteSlice: StateCreator<
  WebsiteSlice,
  [],
  [],
  WebsiteSlice
> = (set, get) => ({
  website: {
    currentWebsite: null,
    savedWebsites: [],
    currentPreviewPage: null,
  },
  
  setCurrentWebsite: (website: GenerationResult | null) => {
    set((state) => ({
      website: {
        ...state.website,
        currentWebsite: website,
        currentPreviewPage: website?.pages[0]?.id || null
      }
    }));
  },
  
  saveWebsite: (website: GenerationResult) => {
    const existingWebsites = get().website.savedWebsites;
    const exists = existingWebsites.some(w => w.websiteUrl === website.websiteUrl);
    
    if (!exists) {
      set((state) => ({
        website: {
          ...state.website,
          savedWebsites: [...state.website.savedWebsites, website]
        }
      }));
    }
  },
  
  deleteWebsite: (websiteId: string) => {
    set((state) => ({
      website: {
        ...state.website,
        savedWebsites: state.website.savedWebsites.filter(w => w.websiteUrl !== websiteId)
      }
    }));
  },
  
  setCurrentPreviewPage: (pageId: string | null) => {
    set((state) => ({
      website: {
        ...state.website,
        currentPreviewPage: pageId
      }
    }));
  }
});

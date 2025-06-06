import { StateCreator } from 'zustand';
import type { 
  GenerationState, 
  GenerationProgress, 
  GenerationError,
  BusinessData 
} from '@/types/generation';
import { v4 as uuidv4 } from 'uuid';
import { generationApi } from '@/services/api';

export interface GenerationSlice {
  // State
  currentGeneration: GenerationState | null;
  generationHistory: GenerationState[];
  isGenerating: boolean;
  
  // Actions
  startGeneration: (businessData: BusinessData) => Promise<void>;
  updateProgress: (progress: GenerationProgress) => void;
  completeGeneration: (result: any) => void;
  failGeneration: (error: GenerationError) => void;
  cancelGeneration: () => void;
  clearCurrentGeneration: () => void;
  
  // WebSocket connection
  wsConnected: boolean;
  setWsConnected: (connected: boolean) => void;
}

export const createGenerationSlice: StateCreator<
  GenerationSlice,
  [],
  [],
  GenerationSlice
> = (set, get) => ({
  // Initial state
  currentGeneration: null,
  generationHistory: [],
  isGenerating: false,  wsConnected: false,
  
  // Actions
  startGeneration: async (businessData: BusinessData) => {
    try {
      set({ isGenerating: true });
      
      // Make a real API call to start the generation
      try {
        // Use the imported generationApi to call the backend
        const response = await generationApi.startGeneration(businessData);
        
        // Use the generation ID from the backend response
        const generationId = response.generation_id || uuidv4();
        
        const newGeneration: GenerationState = {
          id: generationId,
          status: 'in_progress',
          progress: 0,
          startedAt: new Date(),
          businessData,
          steps: [
            {
              id: 'content',
              name: 'Content Generation',
              status: 'pending',
              progress: 0
            },
            {
              id: 'design',
              name: 'Design System',
              status: 'pending',
              progress: 0
            },
            {
              id: 'structure',
              name: 'Website Structure',
              status: 'pending',
              progress: 0
            },
            {
              id: 'quality',
              name: 'Quality Check',
              status: 'pending',
              progress: 0
            }
          ]
        };
        
        set({ currentGeneration: newGeneration });
        
        console.log('Generation started successfully:', response);
      } catch (apiError: any) {
        console.error('API call to start generation failed:', apiError);
        
        // Extract detailed error message from response if available
        const errorMessage = apiError?.response?.data?.detail || 
                            'Failed to start website generation';
        
        const error = new Error(errorMessage);
        throw error;
      }
      
    } catch (error) {
      set({ isGenerating: false });
      throw error;
    }
  },
  
  updateProgress: (progress: GenerationProgress) => {
    const current = get().currentGeneration;
    if (!current) return;
    
    const updatedGeneration: GenerationState = {
      ...current,
      progress: progress.progress,
      steps: current.steps.map(step => 
        step.id === progress.step
          ? { ...step, status: 'in_progress', progress: progress.stepProgress }
          : step
      )
    };
    
    set({ currentGeneration: updatedGeneration });
  },
  
  completeGeneration: (result: any) => {
    const current = get().currentGeneration;
    if (!current) return;
    
    const completedGeneration: GenerationState = {
      ...current,
      status: 'completed',
      progress: 100,
      completedAt: new Date(),
      result,
      steps: current.steps.map(step => ({
        ...step,
        status: 'completed',
        progress: 100,
        completedAt: new Date()
      }))
    };
    
    set({ 
      currentGeneration: completedGeneration,
      generationHistory: [
        completedGeneration,
        ...get().generationHistory
      ],
      isGenerating: false 
    });
  },
    failGeneration: (error: GenerationError) => {
    const current = get().currentGeneration;
    if (!current) return;
    
    const failedGeneration: GenerationState = {
      ...current,
      status: 'failed',
      error,
      completedAt: new Date(),
    };
    
    set({ 
      currentGeneration: failedGeneration,
      isGenerating: false 
    });
  },
  
  cancelGeneration: () => {
    const current = get().currentGeneration;
    if (!current) return;
    
    // Call API to cancel generation using the API service
    generationApi.cancelGeneration(current.id).catch(error => {
      console.error('Failed to cancel generation:', error);
    });
    
    set({ 
      currentGeneration: null,
      isGenerating: false 
    });
  },
  
  clearCurrentGeneration: () => {
    set({ 
      currentGeneration: null,
      isGenerating: false 
    });
  },
  
  setWsConnected: (connected: boolean) => {
    set({ wsConnected: connected });
  },
});

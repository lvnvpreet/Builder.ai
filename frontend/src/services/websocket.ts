import { useAppStore } from '@/store';
import type { GenerationProgress, GenerationError } from '@/types/generation';

class WebSocketService {
  private socket: WebSocket | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectInterval = 1000;
  private generationId: string | null = null;

  connect(generationId: string, token: string) {
    this.generationId = generationId;
    const baseWsUrl = import.meta.env.VITE_WS_URL || 'ws://localhost:8000';
    const wsUrl = `${baseWsUrl}/api/v1/websocket/generation/${generationId}`;
    
    // Close existing connection if any
    if (this.socket) {
      this.socket.close();
    }
    
    this.socket = new WebSocket(wsUrl);
    this.setupEventListeners();
    
    return this.socket;
  }

  private setupEventListeners() {
    if (!this.socket) return;

    this.socket.on('connect', () => {
      console.log('WebSocket connected');
      useAppStore.getState().setWsConnected(true);
      this.reconnectAttempts = 0;
    });

    this.socket.on('disconnect', () => {
      console.log('WebSocket disconnected');
      useAppStore.getState().setWsConnected(false);
      this.handleReconnect();
    });

    this.socket.on('progress_update', (data: GenerationProgress) => {
      console.log('Progress update:', data);
      useAppStore.getState().updateProgress(data);
    });

    this.socket.on('agent_progress', (data) => {
      console.log('Agent progress:', data);
      // Update agent-specific progress
      const progress: GenerationProgress = {
        generationId: data.generationId,
        progress: data.overallProgress || 0,
        step: data.agentId,
        stepProgress: data.progress || 0,
        message: data.message,
        timestamp: new Date()
      };
      
      useAppStore.getState().updateProgress(progress);
    });

    this.socket.on('agent_completed', (data) => {
      console.log('Agent completed:', data);
      // Update agent completion status
      const progress: GenerationProgress = {
        generationId: data.generationId,
        progress: data.overallProgress || 0,
        step: data.agentId,
        stepProgress: 100,
        message: 'Completed',
        timestamp: new Date()
      };
      
      useAppStore.getState().updateProgress(progress);
    });

    this.socket.on('agent_failed', (data) => {
      console.log('Agent failed:', data);
      // Handle agent failure
      const error: GenerationError = {
        message: data.error || 'Agent failed',
        code: 'AGENT_FAILED',
        details: `Agent ${data.agentId} failed: ${data.error}`
      };
      
      useAppStore.getState().failGeneration(error);
    });

    this.socket.on('generation_completed', (data) => {
      console.log('Generation completed:', data);
      useAppStore.getState().completeGeneration(data);
    });

    this.socket.on('generation_failed', (data) => {
      console.log('Generation failed:', data);
      const error: GenerationError = {
        message: data.error || 'Generation failed',
        code: 'GENERATION_FAILED',
        details: data.errorDetails
      };
      
      useAppStore.getState().failGeneration(error);
    });

    this.socket.on('image_selected', (data) => {
      console.log('Image selected:', data);
      // Handle image selection updates
    });

    this.socket.on('quality_progress', (data) => {
      console.log('Quality progress:', data);
      // Update quality check progress
      const progress: GenerationProgress = {
        generationId: data.generationId,
        progress: data.overallProgress || 0,
        step: 'quality',
        stepProgress: data.progress || 0,
        message: data.message,
        timestamp: new Date()
      };
      
      useAppStore.getState().updateProgress(progress);
    });

    this.socket.on('error', (error) => {
      console.error('WebSocket error:', error);
    });
  }

  private handleReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      const delay = this.reconnectInterval * Math.pow(2, this.reconnectAttempts - 1);
      
      console.log(`Attempting to reconnect in ${delay}ms (attempt ${this.reconnectAttempts})`);
      
      setTimeout(() => {
        console.log('Reconnecting...');
        if (this.socket) {
          this.socket.connect();
        }
      }, delay);
    }
  }

  disconnect() {
    if (this.socket) {
      this.socket.disconnect();
      useAppStore.getState().setWsConnected(false);
    }
  }

  emit(event: string, data: any) {
    if (this.socket?.connected) {
      this.socket.emit(event, data);
    }
  }
}

export const websocketService = new WebSocketService();

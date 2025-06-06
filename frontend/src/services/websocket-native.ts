import { useAppStore } from '@/store';
import type { GenerationProgress, GenerationError } from '@/types/generation';

interface WebSocketMessage {
  type: string;
  [key: string]: any;
}

class WebSocketNativeService {
  private socket: WebSocket | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectInterval = 1000;
  private generationId: string | null = null;
  private pingInterval: number | null = null;
    connect(generationId: string) {
    this.generationId = generationId;
    
    // Use the correct WebSocket URL format
    // Make sure this matches your backend WebSocket endpoint
    const baseUrl = import.meta.env.VITE_WS_URL || 'http://localhost:8000';
    const wsProtocol = baseUrl.startsWith('https') ? 'wss' : 'ws';    // Extract the domain and path parts correctly
    let domain;
    let path;
    
    try {
      const urlObj = new URL(baseUrl);
      domain = urlObj.host;
      
      // Always use the correct path to match backend router configuration
      // The backend router is mounted at /api/websocket
      path = '/api/websocket/generation/';
    } catch (error) {
      // Fallback if URL parsing fails
      domain = baseUrl.replace(/^https?:\/\//, '').split('/')[0];
      path = '/api/websocket/generation/';
    }
    
    const wsUrl = `${wsProtocol}://${domain}${path}${generationId}`;
    
    console.log(`Connecting to WebSocket at ${wsUrl}`);
    
    // Close existing connection if any
    this.disconnect();
    
    try {
      this.socket = new WebSocket(wsUrl);
      this.setupEventListeners();
      
      // Setup ping interval to keep connection alive
      this.pingInterval = window.setInterval(() => this.sendPing(), 30000);
      
      return this.socket;
    } catch (error) {
      console.error('Failed to connect to WebSocket:', error);
      this.handleReconnect();
      return null;
    }
  }

  private setupEventListeners() {
    if (!this.socket) return;

    this.socket.onopen = () => {
      console.log('WebSocket connected');
      useAppStore.getState().setWsConnected(true);
      this.reconnectAttempts = 0;
    };

    this.socket.onclose = (event) => {
      console.log(`WebSocket closed: ${event.code} ${event.reason}`);
      useAppStore.getState().setWsConnected(false);
      this.handleReconnect();
    };

    this.socket.onerror = (error) => {
      console.error('WebSocket error:', error);
      // The onclose handler will be called after this
    };

    this.socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data) as WebSocketMessage;
        console.log('WebSocket message received:', data);
        
        switch (data.type) {
          case 'connection':
            // Initial connection confirmation
            break;
            
          case 'progress_update':
            // Handle progress updates
            const progress: GenerationProgress = {
              generationId: data.generation_id || this.generationId || '',
              progress: data.progress || 0,
              step: data.step || 'Unknown',
              stepProgress: data.step_progress || data.progress || 0,
              message: data.message || '',
              timestamp: data.timestamp ? new Date(data.timestamp) : new Date()
            };
            useAppStore.getState().updateProgress(progress);
            break;
            
          case 'generation_complete':
            // Handle generation completion
            useAppStore.getState().completeGeneration({
              generationId: data.generation_id || this.generationId || '',
              websiteData: data.final_website || {},
              qualityScore: data.quality_score || 0
            });
            break;
            
          case 'error':
            // Handle errors
            const error: GenerationError = {
              message: data.message || 'Unknown error',
              code: data.code || 'ERROR',
              details: data.details || ''
            };
            useAppStore.getState().failGeneration(error);
            break;
            
          case 'pong':
            // Pong response to our ping
            console.debug('Received pong from server');
            break;
            
          default:
            console.log(`Unhandled WebSocket message type: ${data.type}`, data);
        }
      } catch (error) {
        console.error('Error parsing WebSocket message:', error, event.data);
      }
    };
  }

  private handleReconnect() {
    // Clear ping interval
    if (this.pingInterval !== null) {
      window.clearInterval(this.pingInterval);
      this.pingInterval = null;
    }
    
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      const delay = this.reconnectInterval * Math.pow(2, this.reconnectAttempts - 1);
      
      console.log(`Attempting to reconnect in ${delay}ms (attempt ${this.reconnectAttempts})`);
      
      setTimeout(() => {
        console.log('Reconnecting...');
        if (this.generationId) {
          this.connect(this.generationId);
        }
      }, delay);
    } else {
      console.error('Max reconnection attempts reached');
      // Notify the user that the connection is permanently lost
      useAppStore.getState().failGeneration({
        message: 'Connection to the server lost',
        code: 'CONNECTION_LOST',
        details: 'Unable to reconnect to the server after multiple attempts'
      });
    }
  }

  disconnect() {
    // Clear ping interval
    if (this.pingInterval !== null) {
      window.clearInterval(this.pingInterval);
      this.pingInterval = null;
    }
    
    if (this.socket) {
      // Only close if the socket is not already closing or closed
      if (this.socket.readyState === WebSocket.OPEN || 
          this.socket.readyState === WebSocket.CONNECTING) {
        this.socket.close();
      }
      this.socket = null;
      useAppStore.getState().setWsConnected(false);
    }
  }

  sendPing() {
    this.sendMessage({ type: 'ping' });
  }

  sendMessage(data: any) {
    if (this.socket?.readyState === WebSocket.OPEN) {
      this.socket.send(JSON.stringify(data));
    } else {
      console.warn('Attempted to send message but WebSocket is not open');
    }
  }
}

export const websocketNativeService = new WebSocketNativeService();

import { useEffect, useRef } from 'react';
import { websocketNativeService } from '@/services/websocket-native';
import { useAppStore } from '@/store';

export const useWebSocket = (generationId: string | null) => {
  const { wsConnected } = useAppStore();
  const connectionRef = useRef<boolean>(false);

  useEffect(() => {
    if (generationId && !connectionRef.current) {
      console.log('Connecting WebSocket for generation:', generationId);
      websocketNativeService.connect(generationId);
      connectionRef.current = true;
    }

    return () => {
      if (connectionRef.current) {
        console.log('Disconnecting WebSocket');
        websocketNativeService.disconnect();
        connectionRef.current = false;
      }
    };
  }, [generationId]);

  const sendMessage = (data: any) => {
    websocketNativeService.sendMessage(data);
  };

  return {
    connected: wsConnected,
    sendMessage,
  };
};

export default useWebSocket;

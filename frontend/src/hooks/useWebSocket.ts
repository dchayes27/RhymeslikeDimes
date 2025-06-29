import { useEffect, useRef, useState, useCallback } from 'react';

interface WebSocketMessage {
  type: string;
  data: any;
}

export const useWebSocket = (url: string) => {
  const [isConnected, setIsConnected] = useState(false);
  const [lastMessage, setLastMessage] = useState<WebSocketMessage | null>(null);
  const ws = useRef<WebSocket | null>(null);

  const sendMessage = useCallback((message: WebSocketMessage) => {
    if (ws.current?.readyState === WebSocket.OPEN) {
      ws.current.send(JSON.stringify(message));
    }
  }, []);

  useEffect(() => {
    const connect = () => {
      try {
        ws.current = new WebSocket(url);

        ws.current.onopen = () => {
          console.log('WebSocket connected');
          setIsConnected(true);
        };

        ws.current.onmessage = (event) => {
          const message = JSON.parse(event.data);
          setLastMessage(message);
        };

        ws.current.onclose = () => {
          console.log('WebSocket disconnected');
          setIsConnected(false);
          // Reconnect after 3 seconds
          setTimeout(connect, 3000);
        };

        ws.current.onerror = (error) => {
          console.error('WebSocket error:', error);
        };
      } catch (error) {
        console.error('Failed to connect WebSocket:', error);
      }
    };

    connect();

    return () => {
      ws.current?.close();
    };
  }, [url]);

  return { isConnected, lastMessage, sendMessage };
};
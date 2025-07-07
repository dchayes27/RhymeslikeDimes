from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, Set
import json
import logging
from app.core.rhyme_engine import RhymeEngine
from app.utils.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class ConnectionManager:
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()
        self.rhyme_engine = RhymeEngine()
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)
        logger.info(f"Client connected. Total connections: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.discard(websocket)
        logger.info(f"Client disconnected. Total connections: {len(self.active_connections)}")
    
    async def handle_message(self, websocket: WebSocket, message: Dict):
        """Handle incoming WebSocket messages."""
        try:
            msg_type = message.get("type")
            data = message.get("data", {})
            
            if msg_type == "analyze":
                bar = data.get("bar", "")
                if bar:
                    fragments = self.rhyme_engine.analyze_bar(bar)
                    await websocket.send_json({
                        "type": "analysis",
                        "data": {
                            "fragments": fragments,
                            "original_bar": bar
                        }
                    })
            
            elif msg_type == "suggestion":
                word = data.get("word", "")
                if word:
                    suggestions = self.rhyme_engine.get_suggestions_for_word(word)
                    await websocket.send_json({
                        "type": "suggestions",
                        "data": {
                            "word": word,
                            "suggestions": suggestions
                        }
                    })
            
            elif msg_type == "ping":
                await websocket.send_json({"type": "pong"})
            
        except Exception as e:
            logger.error(f"Error handling WebSocket message: {str(e)}")
            await websocket.send_json({
                "type": "error",
                "data": {"message": "Failed to process request"}
            })


manager = ConnectionManager()


async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time rhyme analysis."""
    await manager.connect(websocket)
    
    try:
        while True:
            # Receive message
            text_data = await websocket.receive_text()
            message = json.loads(text_data)
            
            # Handle the message
            await manager.handle_message(websocket, message)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
        manager.disconnect(websocket)
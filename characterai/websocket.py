import asyncio
import websockets
import json
import sys
sys.path.append("..")
from simpleaichat.simpleaichat import *
async def handle_websocket(websocket, path):
    async for message in websocket:
        try:
            data = json.loads(message)
            prompt = data.get("prompt", "")
            api_key = data.get("api_key", "sk-1226bc6e75f94b3cba8d8c81dcc8d6f3")
            model = data.get("model", "qwen-turbo")

            ai=AsyncAIChat(api_key=api_key, model=model,console=False)
            result=await ai(prompt) 
            await websocket.send(str(result))
            
        except json.JSONDecodeError:
            error_message = "Invalid JSON format."
            await websocket.send(error_message)



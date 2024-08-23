import asyncio
from fastapi import FastAPI
import uvicorn
import websockets
from communication.http_handler import router
from communication.websocket import handle_websocket

app = FastAPI()
app.include_router(router)
async def main():
    # Set up the WebSocket server
    websocket_server = websockets.serve(handle_websocket, "localhost", 8765)
    
    # Set up the FastAPI server
    config = uvicorn.Config(app, host="localhost", port=8080, log_level="info")
    fastapi_server = uvicorn.Server(config)
    
    print("WebSocket server started on ws://localhost:8765")
    print("HTTP server started on http://localhost:8080")
    
    # Start both servers
    await asyncio.gather(websocket_server, fastapi_server.serve())

if __name__ == "__main__":
    asyncio.run(main())
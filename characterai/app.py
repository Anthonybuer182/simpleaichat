import asyncio
from fastapi import FastAPI, Depends
import uvicorn
from websockets.server import serve as websocket_serve
from mongodb.database import close_db, init_db
from websocket import handle_websocket
from httpapi import router


app = FastAPI()
@app.on_event("startup")
async def startup_event():
    await init_db("mongodb://localhost:27017/", "conversation_database")
    print("MongoDB connected")

@app.on_event("shutdown")
async def shutdown_event():
    await close_db()
    print("MongoDB connection closed")

@app.get("/")
async def root():
    return {"message": "Hello World"}
app.include_router(router)
async def websocket_handler(websocket, path):
    await handle_websocket(websocket)

async def start_websocket_server():
    websocket_server = websocket_serve(websocket_handler, "localhost", 8765)
    await websocket_server

async def start_fastapi_server():
    config = uvicorn.Config(app, host="localhost", port=8080, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

async def main():
    print("WebSocket server started on ws://localhost:8765")
    print("HTTP server started on http://localhost:8080")
    
    # 启动 WebSocket 和 FastAPI 服务器
    await asyncio.gather(start_websocket_server(), start_fastapi_server())

if __name__ == "__main__":
    asyncio.run(main())

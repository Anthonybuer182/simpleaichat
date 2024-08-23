import asyncio
import websockets

async def handle_websocket(websocket, path):
    async for message in websocket:
        print(f"Received message from client: {message}")
        
        # Echo the received message back to the client
        response = f"Echo: {message}"
        await websocket.send(response)
        print(f"Sent message to client: {response}")



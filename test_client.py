import asyncio
import websockets

async def test():
    uri = "ws://127.0.0.1:8000/ws/stream"
    async with websockets.connect(uri) as websocket:
        await websocket.send("hello from glasses")
        response = await websocket.recv()
        print(f"Server replied: {response}")

asyncio.run(test())
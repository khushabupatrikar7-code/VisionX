import asyncio
import websockets
import json

async def test():
    uri = "ws://127.0.0.1:8000/ws/stream"
    async with websockets.connect(uri) as websocket:
        await websocket.send("pretend this is a camera frame")
        response = await websocket.recv()
        parsed = json.loads(response)
        print(f"Server says: {parsed['text']}")

asyncio.run(test())
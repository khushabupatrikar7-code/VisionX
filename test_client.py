import asyncio
import websockets
import json
import sys

async def test(action, image_path):
    uri = "ws://127.0.0.1:8000/ws/stream"
    async with websockets.connect(uri) as websocket:
        await websocket.send(action)
        with open(image_path, "rb") as f:
            image_bytes = f.read()
        await websocket.send(image_bytes)

        response = await websocket.recv()
        parsed = json.loads(response)
        print(f"Server says: {parsed['text']}")

if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else "describe_scene"
    image_path = sys.argv[2] if len(sys.argv) > 2 else "test_image.jpg"
    asyncio.run(test(action, image_path))
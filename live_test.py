import asyncio
import websockets
import json
import cv2
import time

RECORD_DURATION = 12  # simulated total recording length in seconds
INTERVAL = 3           # seconds between each live description

async def test():
    uri = "ws://127.0.0.1:8000/ws/stream"
    async with websockets.connect(uri) as websocket:
        cap = cv2.VideoCapture(0)

        await websocket.send("start_recording")
        print("Recording started (simulating tap-to-start)...")

        start_time = time.time()
        while time.time() - start_time < RECORD_DURATION:
            ret, frame = cap.read()
            if not ret:
                break
            _, frame_bytes = cv2.imencode('.jpg', frame)

            await websocket.send("live_frame")
            await websocket.send(frame_bytes.tobytes())

            response = await websocket.recv()
            parsed = json.loads(response)
            print(f"[Live update] {parsed['text']}")

            time.sleep(INTERVAL)

        cap.release()
        await websocket.send("stop_recording")
        response = await websocket.recv()
        parsed = json.loads(response)
        print(f"[Final] {parsed['text']}")

asyncio.run(test())
import asyncio
import websockets
import json
import cv2
import time

async def test():
    uri = "ws://127.0.0.1:8000/ws/stream"
    async with websockets.connect(uri) as websocket:
        cap = cv2.VideoCapture(0)

        print("Recording 2.5 seconds... hold still, then move/change something")

        ret, start_frame = cap.read()
        cv2.imshow("Recording...", start_frame)
        cv2.waitKey(1)

        time.sleep(2.5)

        ret, end_frame = cap.read()
        cv2.imshow("Recording...", end_frame)
        cv2.waitKey(500)
        cv2.destroyAllWindows()

        cap.release()

        _, start_bytes = cv2.imencode('.jpg', start_frame)
        _, end_bytes = cv2.imencode('.jpg', end_frame)

        await websocket.send("describe_video")
        await websocket.send(start_bytes.tobytes())
        await websocket.send(end_bytes.tobytes())

        response = await websocket.recv()
        parsed = json.loads(response)
        print(f"Server says: {parsed['text']}")

asyncio.run(test())
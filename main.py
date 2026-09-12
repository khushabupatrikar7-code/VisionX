import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Vision X backend is alive"}

@app.websocket("/ws/stream")
async def websocket_stream(websocket: WebSocket):
    await websocket.accept()
    print("Glasses connected!")
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received: {data}")

            # Fake AI response for now — real YOLO plugs in here later
            fake_response = {
                "type": "detection_result",
                "action": "speak",
                "text": "chair detected, 2 meters ahead"
            }
            await websocket.send_text(json.dumps(fake_response))
    except WebSocketDisconnect:
        print("Glasses disconnected.")
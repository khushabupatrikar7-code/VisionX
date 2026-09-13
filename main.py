import json
import base64
import asyncio
from concurrent.futures import ThreadPoolExecutor
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import cv2
import numpy as np
import easyocr
import requests

app = FastAPI()

ocr_reader = easyocr.Reader(['en'])
OLLAMA_URL = "http://localhost:11434/api/generate"

# Blocking AI work runs here so it never freezes the WebSocket connection
executor = ThreadPoolExecutor(max_workers=2)


def decode_frame(image_bytes: bytes):
    np_arr = np.frombuffer(image_bytes, np.uint8)
    return cv2.imdecode(np_arr, cv2.IMREAD_COLOR)


def run_ocr(image_bytes: bytes) -> str:
    frame = decode_frame(image_bytes)
    results = ocr_reader.readtext(frame)
    if not results:
        return "No text found"
    return " ".join([text for (_, text, _) in results])


def run_scene_description(image_bytes: bytes) -> str:
    frame = decode_frame(image_bytes)
    _, buffer = cv2.imencode('.jpg', frame)
    image_b64 = base64.b64encode(buffer).decode('utf-8')

    payload = {
        "model": "moondream",
        "prompt": "Describe this image in detail. Include: the person's apparent gender, any accessories like glasses or jewelry, hair style and color, clothing and its colors, facial expression, and what they appear to be doing. Also describe the background and any objects visible.",
        "images": [image_b64],
        "stream": False,
        "keep_alive": "30m",
        "options": {"num_predict": 150}
    }
    response = requests.post(OLLAMA_URL, json=payload)
    return response.json()["response"]

def run_video_description(start_bytes: bytes, end_bytes: bytes) -> str:
    start_desc = describe_frame_short(start_bytes)
    end_desc = describe_frame_short(end_bytes)
    return f"At first: {start_desc} Then: {end_desc}"


def describe_frame_short(image_bytes: bytes) -> str:
    frame = decode_frame(image_bytes)
    _, buffer = cv2.imencode('.jpg', frame)
    image_b64 = base64.b64encode(buffer).decode('utf-8')

    payload = {
        "model": "moondream",
        "prompt": "Describe this image in one short sentence, under 12 words.",
        "images": [image_b64],
        "stream": False,
        "keep_alive": "30m",
        "options": {"num_predict": 30}
    }
    response = requests.post(OLLAMA_URL, json=payload)
    return response.json()["response"].strip()


@app.get("/")
def read_root():
    return {"message": "Vision X backend is alive"}


@app.websocket("/ws/stream")
async def websocket_stream(websocket: WebSocket):
    await websocket.accept()
    print("Glasses connected!")
    loop = asyncio.get_event_loop()

    try:
        while True:
            # Firmware sends this first: "describe_scene" (short press) or "read_text" (long press)
            action = await websocket.receive_text()
            print(f"Action requested: {action}")

            if action == "describe_video":
                start_bytes = await websocket.receive_bytes()
                end_bytes = await websocket.receive_bytes()
                result_text = await loop.run_in_executor(executor, run_video_description, start_bytes, end_bytes)
            else:
                image_bytes = await websocket.receive_bytes()
                if action == "read_text":
                    result_text = await loop.run_in_executor(executor, run_ocr, image_bytes)
                elif action == "describe_scene":
                    result_text = await loop.run_in_executor(executor, run_scene_description, image_bytes)
                else:
                    result_text = "Unknown action"
            response = {
                "type": action,
                "action": "speak",
                "text": result_text
            }
            await websocket.send_text(json.dumps(response))

    except WebSocketDisconnect:
        print("Glasses disconnected.")
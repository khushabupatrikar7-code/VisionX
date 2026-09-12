import cv2
import easyocr
import pyttsx3
import requests
import base64

tts = pyttsx3.init()
ocr_reader = easyocr.Reader(['en'])

OLLAMA_URL = "http://localhost:11434/api/generate"


def speak(text):
    print(f"Speaking: {text}")
    tts.say(text)
    tts.runAndWait()


def read_text_aloud(frame):
    results = ocr_reader.readtext(frame)
    if not results:
        speak("No text found")
        return
    full_text = " ".join([text for (_, text, _) in results])
    print(f"Text found: {full_text}")
    speak(full_text)


def describe_scene(frame):
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

    print("Asking Moondream...")
    response = requests.post(OLLAMA_URL, json=payload)
    description = response.json()["response"]
    print(f"Moondream says: {description}")
    speak(description)

def main():
    cap = cv2.VideoCapture(0)
    print("Press 'r' to read text aloud, 's' to describe the scene, 'q' to quit.")

    while True:
        ret, frame = cap.read()
        print(f"Frame read success: {ret}")
        if not ret:
            print("Breaking because frame read failed")
            break

        cv2.imshow("Vision X - Laptop Test", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('r'):
            read_text_aloud(frame)
        elif key == ord('s'):
            describe_scene(frame)
        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
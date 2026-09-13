import sounddevice as sd
import soundfile as sf
from faster_whisper import WhisperModel
import pyttsx3

tts = pyttsx3.init()

print("Loading Whisper model...")
model = WhisperModel("small", device="cpu", compute_type="int8")

DURATION = 7
SAMPLE_RATE = 16000

print(f"Recording {DURATION} seconds... speak now in any language")
audio = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1)
sd.wait()
sf.write("speech_test.wav", audio, SAMPLE_RATE)
print("Recording done, translating...")

segments, info = model.transcribe("speech_test.wav", task="translate", vad_filter=True)

full_text = " ".join([segment.text for segment in segments])
print(f"Detected language: {info.language}")
print(f"English translation: {full_text}")

tts.say(full_text)
tts.runAndWait()
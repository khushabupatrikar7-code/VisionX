import sounddevice as sd
import numpy as np

print("Available audio devices:")
print(sd.query_devices())
print(f"\nDefault input device: {sd.query_devices(kind='input')}")

DURATION = 5
SAMPLE_RATE = 16000

print(f"\nRecording {DURATION} seconds... SPEAK LOUDLY now")
audio = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1)
sd.wait()

max_volume = np.abs(audio).max()
print(f"\nMax volume detected: {max_volume}")
if max_volume < 0.01:
    print("⚠️  This is basically silence — your mic likely isn't capturing audio properly")
else:
    print("✓ Real audio signal detected")
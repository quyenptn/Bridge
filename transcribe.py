python - << 'PY'
from faster_whisper import WhisperModel

audio = "/Users/quinn/Desktop/Bridge/Video/01.mp4"
output = "/Users/quinn/Desktop/Bridge/Whisper_outputs/large-v3_01.txt"

print("\n=== Running large-v3 model ===")
model = WhisperModel("large-v3", device="cpu")

segments, info = model.transcribe(audio)
print(f"Detected language: {info.language}, Duration: {info.duration:.1f}s")

with open(output, "w") as f:
    for s in segments:
        f.write(f"[{s.start:.2f}–{s.end:.2f}] {s.text}\n")

print(f"\n✅ Done! Transcript saved to:\n{output}")
PY

import time
from faster_whisper import WhisperModel

audio = "./Audio/01_first60.wav"

# (Label you’ll see in the logs, model name for faster-whisper)
models = [
    # ("turbo",   "deepdml/faster-whisper-large-v3-turbo-ct2"),
    ("turbo",   "turbo"),
    ("large-v3","large-v3"),
    ("medium",  "medium"),
    ("small",   "small"),
]

results = []

for label, model_name in models:
    print("\n" + "="*60)
    print(f"Running model: {label}  ({model_name})")
    print("="*60)

    # load model
    load_start = time.perf_counter()
    model = WhisperModel(model_name, device="cpu")   # keep "cpu" on your Mac
    load_time = time.perf_counter() - load_start
    print(f"Model load time: {load_time:.2f} seconds")

    # transcribe
    start = time.perf_counter()
    segments, info = model.transcribe(audio, language="en")
    # print(ts["text"])
    transcribe_time = time.perf_counter() - start

    # collect text
    text = "".join(segment.text for segment in segments)

    # save transcript
    out_path = f"./Whisper_outputs/{label}/fast-01.txt"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(text)

    # print quick summary
    print(f"Transcription time: {transcribe_time:.2f} seconds")
    print(f"Approx. real-time factor (for 60s audio): {transcribe_time/60:.2f}x")
    print(f"Detected language: {info.language}"
           f"(p={info.language_probability:.2f})")
    print(f"Transcript preview:\n{text[:300]}...\n")

    results.append((label, load_time, transcribe_time, len(text)))

print("\n================ SUMMARY ================")
for label, load_t, trans_t, length in results:
    print(f"{label:8s}  load={load_t:6.2f}s  transcribe={trans_t:6.2f}s  "
          f"chars={length}")
print("========================================")


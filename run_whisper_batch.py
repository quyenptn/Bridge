import time
import whisper

audio = "./Audio/01_first60.wav"

models = [
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
    model = whisper.load_model(model_name, device="cpu")   # keep "cpu" on your Mac
    load_time = time.perf_counter() - load_start
    print(f"Model load time: {load_time:.2f} seconds")

    # transcribe
    start = time.perf_counter()
    ts = model.transcribe(audio, fp16=False)
    print(ts["text"])
    transcribe_time = time.perf_counter() - start

    # save transcript
    out_path = f"./Whisper_outputs/{label}/01.txt"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(ts["text"])

    # print quick summary
    print(f"Transcription time: {transcribe_time:.2f} seconds")
    print(f"Approx. real-time factor (for 60s audio): {transcribe_time/60:.2f}x")
    print(f"Detected language: {ts['language']}")
    print(f"Transcript preview:\n{ts['text'][:300]}...\n")

    results.append((label, load_time, transcribe_time, len(ts["text"])))

print("\n================ SUMMARY ================")
for label, load_t, trans_t, length in results:
    print(f"{label:8s}  load={load_t:6.2f}s  transcribe={trans_t:6.2f}s  "
          f"chars={length}")
print("========================================")


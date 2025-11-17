import os
import time
import csv
from faster_whisper import WhisperModel

# ===== CONFIG =====
AUDIO_DIR = "./Audio"
OUTPUT_ROOT = "./Whisper_outputs"
AUDIO_EXTS = (".wav")

models = [
    ("turbo",   "turbo"),
    ("large-v3","large-v3"),
    ("medium",  "medium"),
    ("small",   "small"),
]
# ==================

# Create output directory
os.makedirs(OUTPUT_ROOT, exist_ok=True)

# Find all audio files
audio_files = [
    f for f in os.listdir(AUDIO_DIR)
    if f.lower().endswith(AUDIO_EXTS)
]
audio_files.sort()

if not audio_files:
    raise RuntimeError("❌ No audio files found in ./Audio")

print("Audio files found:")
for f in audio_files:
    print("  •", f)
    
# CSV file setup
csv_path = os.path.join(OUTPUT_ROOT, "run_summary_fast.csv")
csv_header = [
    "audio_file", "model", "load_time",
    "transcribe_time", "duration",
    "real_time_factor", "text_length"
]

csv_rows = []

# Load all models once
loaded_models = {}
for label, model_name in models:
    print("\n" + "="*60)
    print(f"Loading model: {label} ({model_name})")
    print("="*60)

    start = time.perf_counter()
    model = WhisperModel(model_name, device="cpu")
    load_time = time.perf_counter() - start

    print(f"Loaded {label} in {load_time:.2f}s")
    
    # Process each audio file
    for audio_file in audio_files:
        audio_path = os.path.join(AUDIO_DIR, audio_file)
        base_name, _ = os.path.splitext(audio_file)

        print("\n" + "#"*70)
        print(f"Running {label} on {audio_file}")
        print("#"*70)
        
        # Transcribe
        start = time.perf_counter()
        # ts = model.transcribe(audio_path, fp16=False)
        segments, info = model.transcribe(audio_path, language="en")
        transcribe_time = time.perf_counter() - start
        
        text = "".join(segment.text for segment in segments)

        # Estimate audio duration from last segment
        # segments = ts.get("segments", [])
        if segments:
            duration = segments[-1]["end"]
        else:
            duration = 0.0

        # Compute real-time factor
        rt_factor = transcribe_time / duration if duration > 0 else 0.0

        # Save transcript
        out_dir = os.path.join(OUTPUT_ROOT, label)
        os.makedirs(out_dir, exist_ok=True)

        out_txt_path = os.path.join(out_dir, f"{base_name}_fast.txt")
        with open(out_txt_path, "w", encoding="utf-8") as f:
            f.write(text)

        print(f"→ Transcription time: {transcribe_time:.2f}s")
        print(f"→ Duration: {duration:.2f}s")
        print(f"→ Real-time factor: {rt_factor:.2f}x")

        # Add row to CSV
        csv_rows.append([
            audio_file,
            label,
            f"{load_time:.4f}",
            f"{transcribe_time:.4f}",
            f"{duration:.4f}",
            f"{rt_factor:.4f}",
            str(len(text))
        ])
        
    # loaded_models[label] = (model, load_time)


# # Process each audio file
# for audio_file in audio_files:
#     audio_path = os.path.join(AUDIO_DIR, audio_file)
#     base_name, _ = os.path.splitext(audio_file)

#     print("\n" + "#"*70)
#     print(f"Processing: {audio_file}")
#     print("#"*70)

#     for label, model_name in models:
#         model, load_time = loaded_models[label]

#         print("\n" + "-"*60)
#         print(f"Running {label} on {audio_file}")
#         print("-"*60)

#         # Transcribe
#         start = time.perf_counter()
#         ts = model.transcribe(audio_path, fp16=False)
#         transcribe_time = time.perf_counter() - start

#         # Estimate audio duration from last segment
#         segments = ts.get("segments", [])
#         if segments:
#             duration = segments[-1]["end"]
#         else:
#             duration = 0.0

#         # Compute real-time factor
#         rt_factor = transcribe_time / duration if duration > 0 else 0.0

#         # Save transcript
#         out_dir = os.path.join(OUTPUT_ROOT, label)
#         os.makedirs(out_dir, exist_ok=True)

#         out_txt_path = os.path.join(out_dir, f"{base_name}.txt")
#         with open(out_txt_path, "w", encoding="utf-8") as f:
#             f.write(ts["text"])

#         print(f"→ Transcription time: {transcribe_time:.2f}s")
#         print(f"→ Duration: {duration:.2f}s")
#         print(f"→ Real-time factor: {rt_factor:.2f}x")

#         # Add row to CSV
#         csv_rows.append([
#             audio_file,
#             label,
#             f"{load_time:.4f}",
#             f"{transcribe_time:.4f}",
#             f"{duration:.4f}",
#             f"{rt_factor:.4f}",
#             str(len(ts["text"]))
#         ])

# Write CSV file
with open(csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(csv_header)
    writer.writerows(csv_rows)

print("\n✅ All done!")
print(f"📄 CSV saved to: {csv_path}")

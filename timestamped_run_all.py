import os
import time
import csv
import subprocess

# ========= CONFIG =========
AUDIO_DIR = "./Audio"
OUTPUT_DIR = "./WhisperTS_outputs"
AUDIO_EXTS = (".wav")
LANG = "en"
FIXED_DURATION = 60.0      # fixed duration = 60 seconds
# ==========================


def main():
    # Make sure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Collect audio files
    audio_files = [
        f for f in os.listdir(AUDIO_DIR)
        if f.lower().endswith(AUDIO_EXTS)
    ]
    audio_files.sort()

    if not audio_files:
        raise RuntimeError("❌ No audio files found in ./Audio")

    print("Found audio files:")
    for f in audio_files:
        print("  •", f)

    # Prepare CSV log
    csv_path = os.path.join(OUTPUT_DIR, "whisper_ts_summary.csv")
    csv_header = ["audio_file", "duration_sec", "runtime_sec", "real_time_factor"]
    rows = []

    # === MAIN LOOP ===
    for fname in audio_files:
        audio_path = os.path.join(AUDIO_DIR, fname)
        base_name, _ = os.path.splitext(fname)

        print("\n" + "#" * 70)
        print(f"Processing: {fname}")
        print("#" * 70)

        # FIXED DURATION = 60 seconds
        duration = FIXED_DURATION
        print(f"Using fixed duration: {duration:.2f} s")

        # Run whisper_timestamped and measure time
        start = time.perf_counter()

        cmd = [
            "whisper_timestamped",
            os.path.abspath(audio_path),
            "--language", LANG,
            "--output_dir", OUTPUT_DIR,
            "--output_format", "txt",
            "--detect_disfluencies", "True",
        ]

        print("\nRunning command:")
        print(" ".join(cmd))
        print()

        # run process and PRINT LIVE OUTPUT
        process = subprocess.Popen(
            cmd,
            cwd=OUTPUT_DIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        # print each line while running
        for line in process.stdout:
            print(line.rstrip())

        process.wait()
        runtime = time.perf_counter() - start
        rtf = runtime / duration

        print(f"\nRuntime: {runtime:.2f} seconds")
        print(f"Real-time factor: {rtf:.2f}x")

        # Add row to CSV
        rows.append([
            fname,
            f"{duration:.4f}",
            f"{runtime:.4f}",
            f"{rtf:.4f}",
        ])

    # Write CSV summary after all files processed
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(csv_header)
        writer.writerows(rows)

    print("\n" + "=" * 70)
    print("✅ Done! All files processed.")
    print(f"📄 Summary saved to: {csv_path}")
    print(f"📁 Transcripts saved in: {os.path.abspath(OUTPUT_DIR)}")
    print("=" * 70)


if __name__ == "__main__":
    main()

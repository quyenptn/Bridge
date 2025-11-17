#!/usr/bin/env bash
# Convert all MP4 files in /Video to WAV files in /Audio

SRC_DIR="Video/output_clips"
OUT_DIR="Audio"

mkdir -p "$OUT_DIR"

echo "Scanning $SRC_DIR for .mp4 files..."

found=0
for src in "$SRC_DIR"/55_first60.mp4; do
	# If the pattern didn't match any files, skip
	[ -e "$src" ] || continue
	found=1

	filename=$(basename -- "$src")
	name_no_ext="${filename%.mp4}"
	out="$OUT_DIR/$name_no_ext.wav"

	if [ -e "$out" ]; then
		printf "Skipping (exists): %s -> %s\n" "$src" "$out"
		continue
	fi

	printf "Converting: %s -> %s\n" "$src" "$out"

	# Run ffmpeg; -hide_banner and -loglevel info keep output concise.
	# -y is intentionally not used because we check for existence already.

	if ! ffmpeg -hide_banner -loglevel error -i "$src" "$out"; then
		printf "Error converting %s. Continuing with next file.\n" "$src" >&2
	else
		printf "Done: %s\n" "$out"
	fi
done

if [ "$found" -eq 0 ]; then
	echo "No .mp4 files found in $SRC_DIR. Nothing to do."
else
	echo "All done. Converted missing files to $OUT_DIR/."
fi


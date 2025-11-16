from yt_dlp import YoutubeDL

# --- Your task list (URL, time range, video number) ---
# /Users/quinn/Desktop/Bridge/down_ytb.py
# Task list for batch video downloads (videos 39–60)

TASKS = [
    
    ("https://youtu.be/pBRSZBtirAk?si=rd8BuZth8tEes1_V", "00:04:50-00:05:52", "21"),
]


def hook(d):
    if d.get('status') == 'downloading':
        print(f"[{d.get('elapsed',0):.1f}s] {d.get('_percent_str','?').strip()} "
              f"at {d.get('_speed_str','?')} ETA {d.get('_eta_str','?')}", end="\r")
    elif d.get('status') == 'finished':
        print(f"\nMerging/cutting… {d.get('filename','')}")

# --- Loop through all tasks ---
for url, section, name in TASKS:
    print(f"\n=== Downloading video {name} ===")

    ydl_opts = {
        'format': 'bv*[height<=480]+ba/best',
        'merge_output_format': 'mp4',
        'ratelimit': 500 * 1024,  # 500 KB/s
        'concurrent_fragment_downloads': 4,
        'download_sections': [f'*{section}'],
        'force_keyframes_at_cuts': True,
        'progress_hooks': [hook],
        'outtmpl': f'Bridge_{name}.%(ext)s',  # output filename
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

print("\n✅ All downloads completed.")

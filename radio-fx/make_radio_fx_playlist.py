import os
import random
import librosa

# Directory containing wav files
fx_dir = "radio-fx"
# Output playlist file
playlist_file = "radio-fx/radio-fx.m3u"

# List all .wav files in the directory
wav_files = [f for f in os.listdir(fx_dir) if f.lower().endswith(".wav")]


with open(playlist_file, "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")
    for wav in wav_files:
        print(f"processing {wav}")
        wav_path = os.path.join(fx_dir, wav)
        try:
            duration = librosa.get_duration(filename=wav_path)
            if duration > 1:
                # Pick 5 unique random start times within the file duration
                max_start = int(duration) - 1
                if max_start < 1:
                    starts = [0]
                else:
                    starts = random.sample(range(0, max_start), min(5, max_start))
            else:
                starts = [0]
        except Exception:
            starts = [0]
        for start_time in starts:
            # Escape special characters for M3U (e.g., #, space)
            safe_wav = wav.replace("#", "%23").replace(" ", "%20")
            f.write(f"#EXTVLCOPT:start-time={start_time}\n")
            f.write(f"{safe_wav}\n")

print(f"Playlist written to {playlist_file} with {len(wav_files)} wav files.")

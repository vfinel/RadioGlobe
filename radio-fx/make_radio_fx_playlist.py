import os

# notes that .wave files should be extrated from the zip file
# downloadable from https://drive.google.com/file/d/13xFmD_ltBQFg-plnSqKjVXYcXMsUAvUL/view?usp=sharing

# Directory containing wav files
fx_dir = "radio-fx"

# Output playlist file
playlist_file = "radio-fx/radio-fx.m3u"

# List all .wav files in the directory
wav_files = [f for f in os.listdir(fx_dir) if f.lower().endswith(".wav")]


with open(playlist_file, "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")
    for wav_file in wav_files:
        if wav_file != "oxp.wav":
            # Escape special characters
            safe_wav_file = wav_file.replace("#", "%23").replace(" ", "%20")
            f.write(f"{safe_wav_file}\n")

print(f"Playlist written to {playlist_file} with {len(wav_files)} wav files.")

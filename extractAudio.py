import sys
import ffmpeg

def extract_audio(video_path, audio_path):
    try:
        ffmpeg.input(video_path).output(audio_path, acodec="pcm_s16le", ar="16000").run(overwrite_output=True)
        print(f"✅ Audio extracted: {audio_path}")
    except ffmpeg.Error as e:
        print(f"❌ FFmpeg error: {e}")
        print(f"❌ Output from FFmpeg: {e.stderr.decode()}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("❌ Invalid number of arguments. Expected video path and audio path.")
        sys.exit(1)

    video_path = sys.argv[1]
    audio_path = sys.argv[2]

    extract_audio(video_path, audio_path)

import os
import subprocess

def reprocess_srt():
    video_path = "path/to/file.MOV"
    subtitles_path = "path/to/file.srt"
    output_video_path = "path/to/file_output.MOV"
    
    # Add subtitles to the video
    subprocess.run([
        "ffmpeg",
        "-i", video_path, 
        "-vf", f"subtitles={subtitles_path}:force_style='FontSize=10,MarginV=75'", 
        "-c:a", "copy", 
        output_video_path
    ])

    if os.path.exists(output_video_path):
        print(f"✅ Subtitles added to video: {output_video_path}")
    else:
        print(f"❌ Failed to add subtitles to the video.")

reprocess_srt()

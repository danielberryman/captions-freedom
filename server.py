from flask import Flask, request, jsonify, send_from_directory
import os
import time
import subprocess
from werkzeug.utils import secure_filename
from flask_cors import CORS
import uuid

app = Flask(__name__, static_folder="frontend")
CORS(app)

OUTPUT_DIR = "output"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Increase file upload limit (100MB)
app.config["MAX_CONTENT_LENGTH"] = 100 * 1024 * 1024  # Allow up to 100MB uploads
app.config["ALLOWED_EXTENSIONS"] = {"mp4", "mov", "avi", "mkv"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]

# Route to serve the HTML file
@app.route("/")
def serve_index():
    print("hello", os.getcwd())
    return send_from_directory(os.getcwd(), "index.html")

@app.route("/upload", methods=["POST"])
def upload_video():
    if "video" not in request.files:
        return jsonify({"success": False, "error": "No file uploaded"}), 400

    file = request.files["video"]
    if file.filename == "":
        return jsonify({"success": False, "error": "No selected file"}), 400

    if not allowed_file(file.filename):
        return jsonify({"success": False, "error": "Invalid file type"}), 403
    
    # Create a unique folder for each run using a timestamp or uuid
    run_id = str(uuid.uuid4())  # Create a unique ID for each run
    run_folder = os.path.join(OUTPUT_DIR, run_id)
    os.makedirs(run_folder)

    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = secure_filename(file.filename)
    video_path = os.path.join(run_folder, f"{timestamp}_{filename}")

    file.save(video_path)

    print(f"✅ Video uploaded: {video_path}")

    # Extract audio
    audio_path = video_path.replace(".mp4", ".wav").replace(".MOV", ".wav")
    subprocess.run(["python3", "extractAudio.py", video_path, audio_path])

    if os.path.exists(audio_path):
        print(f"✅ Audio extracted successfully: {audio_path}")
    else:
        print(f"❌ Audio extraction failed: {audio_path}")

    # Convert audio to clean WAV
    clean_audio_path = audio_path.replace(".wav", "_clean.wav")
    subprocess.run(["ffmpeg", "-i", audio_path, "-ac", "1", "-ar", "16000", "-acodec", "pcm_s16le", clean_audio_path])

    if os.path.exists(clean_audio_path):
        print(f"✅ Clean Audio extracted successfully: {clean_audio_path}")
    else:
        print(f"❌ Clean Audio extraction failed: {clean_audio_path}")

    # Generate subtitles
    subtitles_path = video_path.replace(".mp4", ".srt").replace(".MOV", ".srt")
    subprocess.run(["python3", "extractSubtitles.py", clean_audio_path, subtitles_path])

    if os.path.exists(subtitles_path):
        print(f"✅ Subtitles extracted successfully: {subtitles_path}")
    else:
        print(f"❌ Subtitles extraction failed: {subtitles_path}")

        # Add subtitles to the video
    output_video_path = video_path.replace(".MOV", "_output.MOV")
    subprocess.run([
        "ffmpeg",
        "-i", video_path, 
        "-vf", f"subtitles={subtitles_path}", 
        "-c:a", "copy", 
        output_video_path
    ])

    if os.path.exists(output_video_path):
        print(f"✅ Subtitles added to video: {output_video_path}")
    else:
        print(f"❌ Failed to add subtitles to the video.")

    return jsonify({
        "success": True,
        "file_name": os.path.basename(subtitles_path),
        "audio_file": os.path.basename(clean_audio_path),
        "video_file": os.path.basename(output_video_path),
        "file_path": f"/download/{run_id}/{os.path.basename(subtitles_path)}",
        "audio_path": f"/download/{run_id}/{os.path.basename(clean_audio_path)}",
        "video_path": f"/download/{run_id}/{os.path.basename(output_video_path)}"
    })

@app.route("/download/<run_id>/<filename>")
def download_file(run_id, filename):
    # Ensure the file exists in the unique run folder under the output directory
    file_path = os.path.join(OUTPUT_DIR, run_id, filename)
    
    if os.path.exists(file_path):
        # Send the file to the browser for opening with default app (depending on the file type)
        return send_from_directory(os.path.join(OUTPUT_DIR, run_id), filename)
    else:
        return jsonify({"error": "File not found."}), 404

if __name__ == "__main__":
    app.run(debug=True, port=8081)

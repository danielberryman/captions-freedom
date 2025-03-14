# Video Subtitling and Audio Extraction

This project allows you to extract audio, generate subtitles, and add subtitles to video files using FFmpeg and custom Python scripts. It enables you to upload a video, process it, and get back a subtitle file and a video with embedded subtitles.

## Features

- **Extract Audio**: Extracts audio from a video file and converts it into a clean, ready-to-use `.wav` format.
- **Generate Subtitles**: Uses a speech-to-text engine to generate subtitles from the extracted audio.
- **Add Subtitles to Video**: Embeds the generated subtitles back into the original video, allowing the video to play with the subtitles.

## Prerequisites

Before running this project, ensure that you have the following tools installed:

- **Python 3.x**: Install from [python.org](https://www.python.org/)
- **FFmpeg**: Install from [FFmpeg.org](https://ffmpeg.org/)
- **Vosk API (for speech-to-text)**: Install using  
  ```sh
  pip install vosk
  ```

## Installation

### Clone the repository:
```sh
git clone <your-repository-url>
cd <your-repository-name>
```

### Install required Python dependencies:
```sh
pip install -r requirements.txt
```

### Install FFmpeg:
Follow the installation guide for FFmpeg for your system.

### Download Vosk Model:
1. Download a speech recognition model for Vosk from [here](https://alphacephei.com/vosk/models).
2. Extract the model to the `models/` directory in the project.

### Add Fonts for Subtitles (Optional):
If you want to customize the font and style of your subtitles, download a `.ttf` font and place it in the `fonts/` directory. Update the `force_style` parameters in the Python scripts to use your custom font.

## Usage

### 1. Extract Audio from Video:
To extract audio from a video, run the following Python script:
```sh
python extractAudio.py /path/to/video/file /path/to/output/audio.wav
```
This will extract audio from the video and save it as `audio.wav` (or another format if specified).

### 2. Generate Subtitles:
After extracting the audio, you can generate subtitles using the `extractSubtitles.py` script:
```sh
python extractSubtitles.py /path/to/audio.wav /path/to/output/subtitles.srt
```
This will generate the `subtitles.srt` file based on the audio.

### 3. Add Subtitles to Video:
To add the generated subtitles back to the video, use the following command:
```python
subprocess.run([
    "ffmpeg",
    "-i", "/path/to/video/file",
    "-vf", f"subtitles=/path/to/output/subtitles.srt:fontsdir=/path/to/fonts:fontfile=/path/to/fonts/Roboto-Regular.ttf:force_style='FontSize=24,Alignment=2'",
    "-c:a", "copy",
    "/path/to/output/output_video_with_subtitles.MOV"
])
```
This command adds the subtitles to the video, positions them, and sets the font size to `24`. The new video will be saved as `output_video_with_subtitles.MOV`.

## Project Structure
```
.
├── extractAudio.py        # Extract audio from video file
├── extractSubtitles.py    # Generate subtitles from audio
├── models/                # Directory for speech recognition models (Vosk)
├── fonts/                 # Directory for custom subtitle fonts (optional)
├── output/                # Directory for saving output files (audio, subtitles, videos)
├── app.py                 # Flask app to handle file uploads and processing
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

## How It Works

1. **Extract Audio**: The audio is extracted from the video file, converted to a clean `.wav` format (if necessary), and saved.
2. **Generate Subtitles**: Using the Vosk API, the audio file is processed to create an `.srt` subtitle file.
3. **Add Subtitles to Video**: Using FFmpeg, the subtitles are embedded into the original video file, and the new video is saved with the subtitles added.

## API (Flask)

The project includes a simple Flask web application that allows users to upload a video file, and then processes it on the server to generate subtitles and return the download links.

### Endpoints
- **POST `/upload`**: Upload a video file for processing. The server will extract audio, generate subtitles, and add subtitles to the video.
- **GET `/download/<run_id>/<filename>`**: Download the generated subtitle or video file.

### Example Workflow:
1. The user uploads a video file via the Flask interface.
2. The server processes the file, extracting audio and generating subtitles.
3. Once processing is complete, the user can download the subtitles and the video with embedded subtitles from the provided links.

## Troubleshooting

- **Error opening output file**: Ensure that the output directory is valid and that you have write permissions.
- **Font not found**: Make sure the font file exists in the specified path and that the correct path is provided in the FFmpeg command.

## Future Improvements

- Add a UI for video upload and download links.
- Allow customization of subtitle styles through the frontend.
- Support additional languages for subtitle generation.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.


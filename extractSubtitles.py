import sys
import json
import wave
import srt
from vosk import Model, KaldiRecognizer
from datetime import timedelta

# Paths
MODEL_PATH = "/Users/danielberryman/Code/models/vosk/vosk-model-small-en-us-0.15"

# 2️⃣ Transcribe Audio to Text using Vosk
def transcribe_audio(audio_path, model_path, srt_path):
    model = Model(model_path)
    wf = wave.open(audio_path, "rb")
    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)

    subtitles = []
    index = 1
    start_time = None
    last_text = ""

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break

        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            if "result" in result:
                for word in result["result"]:
                    if start_time is None:
                        start_time = timedelta(seconds=word["start"])

                    end_time = timedelta(seconds=word["end"])
                    last_text += " " + word["word"]

                # Append as subtitle block
                subtitles.append(srt.Subtitle(index, start_time, end_time, last_text.strip()))
                index += 1
                start_time = None  # Reset for next subtitle
                last_text = ""

    # Final transcription pass
    final_result = json.loads(rec.FinalResult())
    if "result" in final_result:
        for word in final_result["result"]:
            if start_time is None:
                start_time = timedelta(seconds=word["start"])

            end_time = timedelta(seconds=word["end"])
            last_text += " " + word["word"]

        if last_text.strip():
            subtitles.append(srt.Subtitle(index, start_time, end_time, last_text.strip()))

    # Write subtitles to SRT file
    with open(srt_path, "w") as f:
        f.write(srt.compose(subtitles))

    print(f"✅ Captions saved successfully: {srt_path}")
    return srt_path

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("❌ Invalid number of arguments. Expected audio path and SRT path.")
        sys.exit(1)

    audio_path = sys.argv[1]
    srt_path = sys.argv[2]

    transcribe_audio(audio_path, MODEL_PATH, srt_path)

import os
from vosk import Model

MODEL_PATH = os.getenv("VOSK_MODEL_PATH", "path/to/vosk/vosk-model-small-en-us-0.15")
if not os.path.exists(MODEL_PATH):
    raise ValueError(f"❌ Model path does not exist: {MODEL_PATH}")
else:
    print(f"✅ Model found at: {MODEL_PATH}")

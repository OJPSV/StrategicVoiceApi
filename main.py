from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from faster_whisper import WhisperModel
import tempfile

app = FastAPI()

# Load model once (adjust to your system's power)
model = WhisperModel("base")

@app.post("/transcribe/")
async def transcribe_audio(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    segments, info = model.transcribe(tmp_path)
    transcription = " ".join([seg.text for seg in segments])

    return JSONResponse(content={
        "language": info.language,
        "transcription": transcription
    })

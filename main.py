from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from faster_whisper import WhisperModel
import tempfile
from fastapi.middleware.cors import CORSMiddleware
# Enable CORS for all origins
import uvicorn
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=10000, reload=True)
app = FastAPI()
@app.get("/")
async def root():
    return {"message": "Welcome to the Whisper Transcription API!"}
# 👇 Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use "*" to allow all origins, or restrict to specific ones
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
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

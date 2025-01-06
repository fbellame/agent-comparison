from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from typing import Dict, Any, List
import whisper
import uvicorn

app = FastAPI()

# Load the Whisper model
model = whisper.load_model("large")  # Load Whisper model

@app.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    """
    Endpoint to transcribe audio file with timestamps.
    """
    if not file.content_type.startswith("audio/"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an audio file.")

    try:
        
        # Transcribe the audio file
        result: Dict[str, Any] = model.transcribe(file.filename, task="transcribe", verbose=False)
        segments: List[Dict[str, Any]] = result["segments"]
        
        transcription_with_timestamps = ""
        for segment in segments:
            start: float = segment["start"]
            end: float = segment["end"]
            text: str = segment["text"]
            transcription_with_timestamps += f"[{start:.2f} - {end:.2f}] {text}\n"
        
        return JSONResponse(content={"transcription": transcription_with_timestamps})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred during transcription: {str(e)}")

# Root endpoint for health check
@app.get("/")
async def read_root():
    return {"message": "Welcome to the transcription API!"}

# Function to start the server
def start_server():
    uvicorn.run(
        app,  # The FastAPI app instance
        host="127.0.0.1",  # Specify the host
        port=9090,         # Specify the port
        log_level="info"   # Set the log level
    )

# Start the server when this script is run
if __name__ == "__main__":
    start_server()

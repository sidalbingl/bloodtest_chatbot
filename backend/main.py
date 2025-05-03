from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import uvicorn
import json
import os
from model_handler import model_handler
from pdf_processor import PDFProcessor
from datetime import datetime
import shutil

app = FastAPI(title="Kan Testi Analiz API")

# CORS ayarları - hem localhost hem 127.0.0.1 destekleniyor
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    text: str
    isUser: bool

class AnalysisResult(BaseModel):
    id: str
    date: str
    fileName: str
    results: dict
    summary: str

class ChatRequest(BaseModel):
    text: str

analysis_history: List[AnalysisResult] = []
chat_history = []
pdf_processor = PDFProcessor()

UPLOAD_DIR = "uploads"
PARSED_FILE = "parsed/latest.json"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs("parsed", exist_ok=True)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())

        analysis, summary = pdf_processor.process_pdf(file_path)

        # Parse edilen verileri kaydet
        with open(PARSED_FILE, "w", encoding="utf-8") as f:
            json.dump(analysis, f, indent=4, ensure_ascii=False)

        result = AnalysisResult(
            id=str(len(analysis_history) + 1),
            date=datetime.now().strftime("%Y-%m-%d"),
            fileName=file.filename,
            results=analysis,
            summary=summary
        )
        analysis_history.append(result)
        return {
            "result": result,
            "message": "Merhaba, test sonucunuz yüklendi. Bugün size nasıl yardımcı olabilirim?"
        }
    except Exception as e:
        print(f"Upload error: {str(e)}")
        raise HTTPException(status_code=500, detail="PDF yükleme ve analiz sırasında bir hata oluştu.")

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        response = model_handler.process_text(request.text)
        chat_history.append({
            "user": request.text,
            "bot": response
        })
        return {"response": response}
    except Exception as e:
        print(f"Chat error: {str(e)}")
        raise HTTPException(status_code=500, detail="Sohbet sırasında bir hata oluştu.")

@app.get("/history")
async def get_history():
    return {"history": chat_history}

if __name__ == "__main__":
    print("🚀 FastAPI sunucusu başlatılıyor...")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
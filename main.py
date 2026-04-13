import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware


origins = [
    "http://localhost:3000",
    "*",
]


load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],  
)

class ChatRequest(BaseModel):
    message: str

@app.post("/api/chat")
async def chat_with_taurus(request: ChatRequest):
    try:
        model = genai.GenerativeModel(
            model_name="gemma-4-31b-it",
        )

        response = model.generate_content(request.message)
        
        return {"reply": response.text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
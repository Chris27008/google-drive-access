from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import os

# Imposta la chiave API di OpenAI dalle variabili d'ambiente
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("La variabile d'ambiente OPENAI_API_KEY non è impostata")

app = FastAPI(title="Chatbot API")

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(req: ChatRequest):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Sei un assistente utile."},
                {"role": "user", "content": req.message},
            ],
        )
        answer = response.choices[0].message["content"].strip()
        return {"response": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

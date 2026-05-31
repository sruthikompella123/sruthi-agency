# main.py
import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from agents.property_advisor_agent import PropertyAdvisorAgent

load_dotenv()

app = FastAPI(title="Sruthi Agency Property Advisor")

API_KEY = os.getenv("GROQ_API_KEY", "")

if not API_KEY or API_KEY == "your_groq_api_key_here":
    print("\n⚠️  WARNING: GROQ_API_KEY not set in .env file!")
    print("   Get your free key from console.groq.com\n")

agent = PropertyAdvisorAgent(api_key=API_KEY)


class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: list[Message]

class ChatResponse(BaseModel):
    reply: str
    chips: list[str] = []


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "message": "Sruthi Agency Chatbot is running!",
        "api_key_set": bool(API_KEY and API_KEY != "your_groq_api_key_here")
    }


@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    if not API_KEY or API_KEY == "your_groq_api_key_here":
        raise HTTPException(
            status_code=500,
            detail="GROQ_API_KEY is not set. Please add it to your .env file."
        )

    if not request.messages:
        raise HTTPException(status_code=400, detail="No messages provided.")

    history = [{"role": m.role, "content": m.content} for m in request.messages]

    try:
        result = agent.run(history)
        return ChatResponse(reply=result["reply"], chips=result.get("chips", []))
    except Exception as e:
        print(f"Agent error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
def serve_frontend():
    return FileResponse("frontend/index.html")


if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*50)
    print("  Sruthi Agency – Property Advisor Chatbot")
    print("  Powered by Groq (Free & Fast!)")
    print("="*50)
    print("  Open this in your browser:")
    print("  → http://localhost:8000")
    print("\n  API Docs:")
    print("  → http://localhost:8000/docs")
    print("="*50 + "\n")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

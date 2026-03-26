from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import diagnose, chat
import uvicorn

app = FastAPI(
    title="PlantDocBot API",
    description="AI Plant Disease Diagnosis via Image and Text",
    version="1.0.0"
)

# ── CORS (allows React frontend to talk to backend) ──────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# ── Routers ──────────────────────────────────────────────
app.include_router(diagnose.router, prefix="/api/diagnose", tags=["Diagnosis"])
app.include_router(chat.router,     prefix="/api/chat",     tags=["Chat"])

@app.get("/")
def root():
    return {"message": "🌿 PlantDocBot API is running!"}

@app.get("/api/health")
def health():
    return {"status": "healthy", "version": "1.0.0"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
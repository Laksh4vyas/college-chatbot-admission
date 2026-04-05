from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import router
from app.utils.ml_loader import ml_loader

app = FastAPI(
    title="College Admission Chatbot API",
    description="Backend API for the College Admission Chatbot, featuring ML soft-voting intent prediction.",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the actual frontend origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    # Pre-load ML models on startup
    ml_loader.load_models()

app.include_router(router)

@app.get("/")
def root():
    return {"message": "Welcome to the College Admission Chatbot API"}

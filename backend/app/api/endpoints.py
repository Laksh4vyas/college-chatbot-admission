from fastapi import APIRouter
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chatbot import process_chat

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    result = process_chat(request.message)
    return ChatResponse(**result)

@router.get("/dashboard-data")
async def dashboard_data():
    # In a real app, this would query a database tracking the model metrics
    # Here we return dummy metrics for the dashboard
    return {
        "accuracy": 0.89,
        "errorRate": 0.11,
        "requestsServed": 1432,
        "averageConfidence": 0.92,
        "activeModels": ["Model A (RF)", "Model B (LR)", "Model C (NB)"]
    }

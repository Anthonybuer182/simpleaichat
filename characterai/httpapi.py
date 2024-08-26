from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import sys
sys.path.append("..")
from simpleaichat.simpleaichat import *

router = APIRouter()
class GreetRequest(BaseModel):
    prompt: str
    model:str = "qwen-turbo"
    api_key:str = "sk-1226bc6e75f94b3cba8d8c81dcc8d6f3"

@router.post("/api/greet")
async def greet(request: GreetRequest):
    ai=AsyncAIChat(api_key=request.api_key, model=request.model,console=False)
    result=await ai(request.prompt)
    return JSONResponse(content=str(result))

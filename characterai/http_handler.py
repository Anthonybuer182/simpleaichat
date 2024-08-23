from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel

router = APIRouter()
class GreetRequest(BaseModel):
    prompt: str
@router.post("/api/greet")
async def greet(request: GreetRequest):
    ## 调用get_answer
    result = ""
    response_data = {"message": f"Hello, {result}"}
    return JSONResponse(content=response_data)

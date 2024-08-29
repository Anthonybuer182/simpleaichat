from pydantic import BaseModel

class GreetRequest(BaseModel):
    prompt: str
    model: str = "qwen-turbo"
    api_key: str = "sk-1226bc6e75f94b3cba8d8c81dcc8d6f3"
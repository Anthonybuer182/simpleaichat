from typing import Optional
from pydantic import BaseModel

class ChatRequest(BaseModel):
    session_id: str
    prompt: str
    model: str = "qwen-turbo"
    api_key: str = "sk-1226bc6e75f94b3cba8d8c81dcc8d6f3"

class Character(BaseModel):
    name: str = ""
    gender: str = ""
    age: str = ""
    personality: str = ""
    voice: str = ""
    profession: str = ""
    hobbies: str = ""
    style: str = ""
    goal: str = ""

class CharacterRequest(BaseModel):
    model: str = "qwen-turbo"
    api_key: str = "sk-1226bc6e75f94b3cba8d8c81dcc8d6f3"
    prompt: str = "很高兴在此与你相遇"
    character: Character

class ImageGenerateRequest(BaseModel):
    model: str = ""
    prompt: str

class TaskRequest(BaseModel):
    model: str = ""
    task_id: str

class AudioGenerateRequest(BaseModel):
    model: str = ""
    prompt: str

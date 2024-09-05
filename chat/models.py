from typing import Optional
from pydantic import BaseModel

class ChatRequest(BaseModel):
    session_id: str = ""
    prompt: str
    model: str = ""
    api_key: str = ""

class Character(BaseModel):
    name: str
    gender: str
    age: str
    personality: str
    voice: str
    profession: str
    hobbies: str
    style: str
    goal: str

class ImageGenerateRequest(BaseModel):
    model: str = ""
    prompt: str

class TaskRequest(BaseModel):
    model: str = ""
    task_id: str

class AudioGenerateRequest(BaseModel):
    model: str = ""
    prompt: str

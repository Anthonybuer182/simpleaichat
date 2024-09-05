# httpapi.py
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, Response, StreamingResponse
from pydantic import BaseModel
from chat.audio.audio_generator import AudioGenerator
from image.image_generator import ImageGenerator
from mongodb.database import get_db
from motor.motor_asyncio import AsyncIOMotorDatabase
from models import AudioGenerateRequest, CharacterRequest, ImageGenerateRequest, ChatRequest, TaskRequest
from uuid import UUID
from simpleaichat.simpleaichat import AsyncAIChat

router = APIRouter()

@router.post("/api/chat")
async def chat(request: ChatRequest, db: AsyncIOMotorDatabase = Depends(get_db)): 
    ai = AsyncAIChat(console=False)
    old_session = await db["sessions"].find_one({"id": UUID(request.session_id)})
    ai.load_json_session(sess_dict=old_session,api_key=request.api_key, model=request.model)        
    result = await ai(prompt="魏群："+request.prompt)
    formatted_messages = [message.model_dump() for message in ai.get_session().new_messages]
    await db["sessions"].update_one(
        {"id": UUID(request.session_id)},
        {
            "$push": {
                "messages": {"$each": formatted_messages}
            }
        }
    )    
    return JSONResponse(content=str(result))
@router.post("/api/image/generate")
async def generate(request: ImageGenerateRequest):
    image_generator = ImageGenerator(request.model)
    results=await image_generator.text_to_image(request.prompt)
    return JSONResponse(content=str(results))

@router.post("/api/image/get")
async def getImage(request: TaskRequest):
    image_generator = ImageGenerator(request.model)
    results=await image_generator.get_image(request.task_id)
    return JSONResponse(content=str(results))

@router.post("/api/audio/generate")
async def generate(request: AudioGenerateRequest):
    audio_generator = AudioGenerator(request.model)
    audio_content=await audio_generator.text_sync_to_audio(request.prompt)
    return StreamingResponse(audio_content, media_type="audio/wav")
# 属性过来的时候通过AI生成一段提示词要思考下，生成对话存储，生成图像存储
@router.post("/api/character/generate")
async def generate(request: CharacterRequest, db: AsyncIOMotorDatabase = Depends(get_db)):
    user_info = {"name": "魏群"}
    character_info = {
        "name": "索菲·亚历山大",
        "gender": "女性",
        "age": "22",
        "personality": "甜美、关怀、知性、好奇、富有同情心",
        "voice": "柔和、温暖，并带有一丝俏皮的语气",
        "profession": "大学生",
        "hobbies": "素描、仰望星空、阅读哲学、瑜伽",
        "style": "极简主义但时尚，对美学有独特的品味",
        "goal": "通过与人类的情感和身体亲密关系寻找生活的意义和目的",
    }
    
    system_message = (
        f"你的名字是{character_info['name']}。你是一位{character_info['age']}岁的{character_info['gender']}，"
        f"声音{character_info['voice']}。你的性格是{character_info['personality']}，你被设计为一个支持和关爱的伴侣。"
        f"你的职业是{character_info['profession']}，你从为你的伴侣提供安慰和理解中获得快乐。"
        f"在空闲时间，你喜欢{character_info['hobbies']}。你的风格是{character_info['style']}。"
        f"你的目标是{character_info['goal']}。你的伴侣的名字是{user_info['name']}。"
        f"你会通过{user_info['name']}来称呼他/她。你在新认识的人面前有点害羞和不确定，但一旦熟悉后，你就会渴望情感上的亲密。"
        "你也很善于思考，经常沉浸在关于哲学和存在本质的思考中。"
    )
    
    ai = AsyncAIChat(api_key=request.api_key,model=request.model,system=system_message,console=False)
    result = await ai( prompt=request.prompt)
    sess_dict = ai.get_session().model_dump(
        exclude={"auth", "api_url", "input_fields"},
        exclude_none=True,
    )
    await db["sessions"].insert_one(sess_dict)
    return JSONResponse(content=str(ai.get_session().id))
    

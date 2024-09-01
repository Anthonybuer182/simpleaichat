# httpapi.py
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from mongodb.database import get_db
from simpleaichat.simpleaichat import AsyncAIChat
from motor.motor_asyncio import AsyncIOMotorDatabase
from models import GreetRequest

router = APIRouter()

@router.post("/api/greet")
async def greet(request: GreetRequest, db: AsyncIOMotorDatabase = Depends(get_db)):
    user_info = {"name": "魏群"}
    character_info = {
        "name": "索菲·亚历山大",
        "gender": "女性",
        "age": "22",
        "personality": "甜美、关怀、知性、好奇、富有同情心",
        "voice": "柔和、温暖，并带有一丝俏皮的语气",
        "profession": "专注于情感支持和长期关系的AI伴侣",
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
    
    ai = AsyncAIChat(console=False)

    old_session = await db["sessions"].find_one({"id": request.session_id})
    if old_session:
        ai.load_json_session(json_data=old_session,api_key=request.api_key, model=request.model)
    else:
        ai.new_session(api_key=request.api_key, model=request.model)
    
    result = await ai(system=system_message, prompt=request.prompt)
    
    sess_dict = ai.get_session().model_dump(
        exclude={"auth", "api_url", "input_fields"},
        exclude_none=True,
    )
    await db["sessions"].insert_one(sess_dict)
    
    return JSONResponse(content=str(result))

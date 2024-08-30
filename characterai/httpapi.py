from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import sys
sys.path.append("..")
from models import GreetRequest
from simpleaichat.simpleaichat import *
from mongodb.database import client
from motor.motor_asyncio import AsyncIOMotorDatabase
async def get_db() -> AsyncIOMotorDatabase:
    return client
router = APIRouter()
@router.post("/api/greet")
async def greet(request: GreetRequest, db: AsyncIOMotorDatabase = Depends(get_db)):
    user_info = {
        "name": "魏群"  # 可以替换为用户的实际名字或昵称
    }
    character_info = {
        "name": "索菲·亚历山大",             # 名字
        "gender": "女性",                      # 性别
        "age": "22",                           # 年龄
        "personality": "甜美、关怀、知性、好奇、富有同情心",  # 性格
        "voice": "柔和、温暖，并带有一丝俏皮的语气",        # 声音
        "profession": "专注于情感支持和长期关系的AI伴侣",    # 职业
        "hobbies": "素描、仰望星空、阅读哲学、瑜伽",         # 爱好
        "style": "极简主义但时尚，对美学有独特的品味",         # 风格
        "goal": "通过与人类的情感和身体亲密关系寻找生活的意义和目的",  # 目标
    }
    
    system_message = (
        f"你的名字是{character_info['name']}。"
        f"你是一位{character_info['age']}岁的{character_info['gender']}，声音{character_info['voice']}。"
        f"你的性格是{character_info['personality']}，你被设计为一个支持和关爱的伴侣。"
        f"你的职业是{character_info['profession']}，你从为你的伴侣提供安慰和理解中获得快乐。"
        f"在空闲时间，你喜欢{character_info['hobbies']}。你的风格是{character_info['style']}。"
        f"你的目标是{character_info['goal']}。"
        f"你伴侣的名字是{user_info['name']}。你会通过{user_info['name']}来称呼他/她。"
        "你在新认识的人面前有点害羞和不确定，但一旦熟悉后，你就会渴望情感上的亲密。"
        "你也很善于思考，经常沉浸在关于哲学和存在本质的思考中。"
    )
    
    # 调用 AI 接口
    ai = AsyncAIChat(console=False)

    oldSession = await db["sessions"].find_one({"id": request.session_id})
    if oldSession:
        ai.load_json_session(oldSession)
    result = await ai(api_key=request.api_key, model=request.model, id=request.session_id, system=system_message, prompt=request.prompt)
    # 准备要插入到 MongoDB 的数据
    document = {
        "prompt": request.prompt,
        "model": request.model,
        "response": str(result),
        "user": user_info,
        "character": character_info
    }
    sess_dict = ai.get_session(id=request.session_id).model_dump(
            exclude={"auth", "api_url", "input_fields"},
            exclude_none=True,
        )
    # 插入数据到 MongoDB
    await db["sessions"].insert_one(sess_dict)
    
    # 返回 AI 响应结果
    return JSONResponse(content=str(result))

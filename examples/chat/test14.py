import sys
sys.path.append("..")
from simpleaichat.simpleaichat import *
from pydantic import BaseModel, Field
from typing import List, Literal, Optional, Union
import orjson
from simpleaichat.simpleaichat.utils import fd

# gpt-3.5-turbo-0125
# Ee1imTXK7hDwDM1aFa0337029aD8421bA27882E038CbA163

model="gpt-3.5-turbo-0125"
apy_key= "sk-Ee1imTXK7hDwDM1aFa0337029aD8421bA27882E038CbA163"
system_prompt = """您是世界知名的桌面角色扮演游戏（RPG）游戏大师（GM）。

为用户提供的设置编写设置描述和两个字符表。

您必须遵守的规则：
-始终以 80 年代奇幻小说的风格写作。
-您创建的所有名称必须具有创意且独特。总是颠覆期望。
-在您的回复中包含尽可能多的信息。"""
ai = AIChat(
    api_key=apy_key,
    console=False,
    save_messages=False,  # with schema I/O, messages are never saved
    model=model,
    system=system_prompt
)

class player_character(BaseModel):
    name: str = Field(description="角色名")
    race: str = Field(description="角色种族")
    job: str = Field(description="角色列别/职业")
    story: str = Field(description="三句话描述任务历史")
    feats: List[str] = Field(description="任务功绩")
class write_ttrpg_setting(BaseModel):
    """编写一款有趣且创新的TTRPG"""

    description: str = Field(
        description="用游戏主持人（DM）的口吻详细描述设定"
    )
    name: str = Field(description="设置名称")
    pcs: List[player_character] = Field(description="TTRPG的玩家角色")

response_structured = ai(
    "葫芦娃和奥特曼", output_schema=write_ttrpg_setting
)

# orjson.dumps preserves field order from the ChatGPT API
print("output",orjson.dumps(response_structured, option=orjson.OPT_INDENT_2).decode())


# 格式化结果
system_prompt_event  = """您是世界知名的桌面角色扮演游戏（RPG）游戏大师（GM）。

使用输入的数据，写一个完整的三幕故事，包含10个事件，并且要有一个令人震惊的结局反转。玩家角色将作为一个团队，去对抗一种新兴的邪恶力量。

在第二个事件中，必须形成团队。

您必须遵守的规则：
-始终以 80 年代奇幻小说的风格写作。
-您创建的所有名称必须具有创意且独特。总是颠覆期望。"""
ai_2 = AIChat(
    api_key=apy_key,
    console=False,
    save_messages=False,  # with schema I/O, messages are never saved
    model=model,
    system=system_prompt_event 
)

input_ttrpg = write_ttrpg_setting.model_validate(response_structured)
class Dialogue(BaseModel):
    character_name: str = fd("角色名称")
    dialogue: str = fd("来自角色的对话")


class Setting(BaseModel):
    description: str = fd(
        "详细的设置或事件描述，例如阳光明媚。"
    )


class Event(BaseModel):
    type: Literal["setting", "conversation"] = fd(
        "事件是场景设置还是NPC对话"
    )
    data: Union[Dialogue, Setting] = fd("事件数据")


class write_ttrpg_story(BaseModel):
    """编写屡获殊荣的 TTRPG 故事"""

    events: List[Event] = fd("TTRPG 战役中的所有事件。")

response_story  = ai_2(
    input_ttrpg, input_schema=write_ttrpg_setting, output_schema=write_ttrpg_story
)

# orjson.dumps preserves field order from the ChatGPT API
print("output2",orjson.dumps(response_story , option=orjson.OPT_INDENT_2).decode())
from typing import Any, Dict, List, Union
import orjson
from httpx import AsyncClient, Client
from pydantic import HttpUrl
from .models import ChatMessage, ChatSession
from .utils import remove_a_key

# 定义 QwenSession 类，继承自 ChatSession
class QwenSession(ChatSession):
    # 设置 API URL
    api_url: HttpUrl = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    # 定义输入字段
    input_fields: set = {"role", "content", "name"}
    # 系统消息的默认内容
    system: str = "You are a helpful assistant."
    # 默认参数
    params: Dict[str, Any] = {"temperature": 0.7}

    # 准备请求的函数
    def prepare_request(
        self,
        prompt: str,
        system: str = None,
        params: Dict[str, Any] = None,
        stream: bool = False,
        input_schema: Any = None,
        output_schema: Any = None,
    ):
        # 设置请求头
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.auth['api_key'].get_secret_value()}",
        }

        # 创建系统消息
        system_message = ChatMessage(role="system", content=system or self.system)
        # 创建用户消息
        user_message = ChatMessage(role="user", content=prompt)

        # 获取生成参数
        gen_params = params or self.params
        # 构建请求数据
        data = {
            "model": self.model,
            "messages": [system_message.dict(), user_message.dict()],
            "stream": stream,
            **gen_params,
        }

        return headers, data, user_message

    # 同步生成响应
    def gen(
        self,
        prompt: str,
        client: Union[Client, AsyncClient],
        system: str = None,
        save_messages: bool = None,
        params: Dict[str, Any] = None,
    ):
        # 准备请求
        headers, data, user_message = self.prepare_request(prompt, system)

        # 发送请求并获取响应
        response = client.post(self.api_url, json=data, headers=headers)
        result = response.json()

        try:
            # 获取生成的内容
            content = result["choices"][0]["message"]["content"]
            # 创建助手消息
            assistant_message = ChatMessage(
                role=result["choices"][0]["message"]["role"],
                content=content,
            )
            # 添加消息到会话
            self.add_messages(user_message, assistant_message, save_messages)
            return content
        except KeyError:
            raise KeyError(f"No AI generation: {result}")

    # 异步生成响应
    async def gen_async(
        self,
        prompt: str,
        client: Union[Client, AsyncClient],
        system: str = None,
        save_messages: bool = None,
        params: Dict[str, Any] = None,
    ):
        # 准备请求
        headers, data, user_message = self.prepare_request(prompt, system)

        # 异步发送请求并获取响应
        async with client.post(self.api_url, json=data, headers=headers) as response:
            result = await response.json()

            try:
                # 获取生成的内容
                content = result["choices"][0]["message"]["content"]
                # 创建助手消息
                assistant_message = ChatMessage(
                    role=result["choices"][0]["message"]["role"],
                    content=content,
                )
                # 添加消息到会话
                self.add_messages(user_message, assistant_message, save_messages)
                return content
            except KeyError:
                raise KeyError(f"No AI generation: {result}")

    # 处理流式响应
    async def stream_async(
        self,
        prompt: str,
        client: Union[Client, AsyncClient],
        system: str = None,
        save_messages: bool = None,
        params: Dict[str, Any] = None,
    ):
        # 准备请求
        headers, data, user_message = self.prepare_request(prompt, system, stream=True)

        # 开始流式请求
        async with client.stream("POST", self.api_url, json=data, headers=headers) as response:
            content = []
            async for chunk in response.aiter_lines():
                if len(chunk) > 0 and chunk != "[DONE]":
                    chunk_dict = orjson.loads(chunk[6:])  # 去除前缀
                    delta = chunk_dict["choices"][0]["delta"].get("content")
                    if delta:
                        content.append(delta)
                        yield {"delta": delta, "response": "".join(content)}

            # 创建助手消息
            assistant_message = ChatMessage(role="assistant", content="".join(content))
            # 添加消息到会话
            self.add_messages(user_message, assistant_message, save_messages)

        return assistant_message

    # 生成带工具的响应
    def gen_with_tools(
        self,
        prompt: str,
        tools: List[Any],
        client: Union[Client, AsyncClient],
        system: str = None,
        save_messages: bool = None,
        params: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        # 选择工具并生成上下文
        tools_list = "\n".join(f"{i+1}: {f.__doc__}" for i, f in enumerate(tools))
        tool_prompt_format = tool_prompt.format(tools=tools_list)

        # 生成工具索引
        tool_idx = int(self.gen(prompt, client=client, system=tool_prompt_format, save_messages=False, params={"temperature": 0.0, "max_tokens": 1}))

        # 如果没有选择工具，进行标准生成
        if tool_idx == 0:
            return {
                "response": self.gen(prompt, client=client, system=system, save_messages=save_messages, params=params),
                "tool": None,
            }
        
        # 选择工具并生成上下文
        selected_tool = tools[tool_idx - 1]
        context_dict = selected_tool(prompt)
        if isinstance(context_dict, str):
            context_dict = {"context": context_dict}

        context_dict["tool"] = selected_tool.__name__

        # 使用上下文生成新的响应
        new_system = f"{system or self.system}\n\nYou MUST use information from the context in your response."
        new_prompt = f"Context: {context_dict['context']}\n\nUser: {prompt}"

        context_dict["response"] = self.gen(new_prompt, client=client, system=new_system, save_messages=False, params=params)

        # 添加用户消息和助手响应
        user_message = ChatMessage(role="user", content=prompt)
        assistant_message = ChatMessage(role="assistant", content=context_dict["response"])
        self.add_messages(user_message, assistant_message, save_messages)

        return context_dict
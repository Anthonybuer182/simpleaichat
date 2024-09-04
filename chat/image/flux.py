from chat.image.base import ImageGeneration
from pydantic import HttpUrl
from httpx import AsyncClient

from chat.models import ImageGenerateRequest
from simpleaichat.utils import async_client
class FluxGeneration(ImageGeneration):
    generate_url: HttpUrl = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis"
    image_url: HttpUrl = "https://dashscope.aliyuncs.com/api/v1/tasks/"
    api_key: str = "sk-1226bc6e75f94b3cba8d8c81dcc8d6f3"
    parameters = {
        "size": "1024*1024",
        "seed":42,
        "steps":4
    }
    client: AsyncClient = async_client()
    async def text_to_image(self, request:ImageGenerateRequest):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "X-DashScope-Async": "enable",
        }
        data = {
            "model": request.model,
            "input": {"prompt":request.prompt},
            "parameters":self.parameters
        }
        r = await self.client.post(
            str(self.generate_url),
            json=data,
            headers=headers,
            timeout=None,
        )
        r = r.json()
        try:
            task_status = r["output"]["task_status"]
            print(f"Model {request.model}: Image generation status: {task_status}")
            task_id = r["output"]["task_id"]
        except Exception as e:
            print(f"Model {request.model}: Failed to generate image for prompt: {request.prompt}, error: {e}")
        return await self.get_image(task_id)

    async def image_to_image(self, data):
        pass

    async def get_image(self, task_id):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        r = await self.client.get(
            self.image_url+task_id,
            headers=headers,
            timeout=None,
        )
        r = r.json()
        try:
            results = r["output"]["results"]
        except Exception as e:
            print(f"Failed to get image for task {task_id}, error: {e}")
        return [result['url'] for result in results]


from http import HTTPStatus
from pathlib import PurePosixPath
import dashscope
import requests
from chat.image.base import ImageGeneration
from urllib.parse import urlparse, unquote
from chat.models import ImageGenerateRequest

class FluxGenerationSDK(ImageGeneration):
    api_key: str = "sk-1226bc6e75f94b3cba8d8c81dcc8d6f3"
    async def text_to_image(self, text):
        rsp = dashscope.ImageSynthesis.call(api_key= self.api_key,model=self.model,
                                        prompt=text,
                                        size='1024*1024')
        if rsp.status_code == HTTPStatus.OK:
            return [result.url for result in rsp.output.results]
            print(rsp.output)
            print(rsp.usage)
            # save file to current directory
            # for result in rsp.output.results:
            #     file_name = PurePosixPath(unquote(urlparse(result.url).path)).parts[-1]
            #     with open('./%s' % file_name, 'wb+') as f:
            #         f.write(requests.get(result.url).content)
        else:
            print('Failed, status_code: %s, code: %s, message: %s' %
                (rsp.status_code, rsp.code, rsp.message))


    async def image_to_image(self, data):
        pass

    async def get_image(self, task_id):
        pass


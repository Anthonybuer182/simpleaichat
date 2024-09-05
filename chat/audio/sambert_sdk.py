import dashscope
from dashscope.audio.tts import SpeechSynthesizer
from chat.audio.base import AudioGeneration
from chat.models import AudioGenerateRequest
from playsound import playsound
from io import BytesIO
class SambertGenerationSDK(AudioGeneration):
    api_key: str = "sk-1226bc6e75f94b3cba8d8c81dcc8d6f3"
    async def text_sync_to_audio(self, text:str):
        dashscope.api_key = self.api_key

        result = SpeechSynthesizer.call(model=self.model,
                                        text=text,
                                        sample_rate=48000,
                                        format='wav')
        audio_data = result.get_audio_data()
        # if audio_data is not None:
        #     with open('output.wav', 'wb') as f:
        #         f.write(result.get_audio_data())
        #     playsound('output.wav')
        print(' get response: %s' % (result.get_response()))

        return BytesIO(audio_data)

    async def audio_sync_to_text(self, audio):
        pass

    async def text_stream_to_audio(self, text):
        pass


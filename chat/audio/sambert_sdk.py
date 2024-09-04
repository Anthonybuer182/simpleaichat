import dashscope
from dashscope.audio.tts import SpeechSynthesizer
from chat.audio.base import AudioGeneration
from chat.models import AudioGenerateRequest
from playsound import playsound
class SambertGenerationSDK(AudioGeneration):
    api_key: str = "sk-1226bc6e75f94b3cba8d8c81dcc8d6f3"
    async def text_sync_to_audio(self, request:AudioGenerateRequest):
        dashscope.api_key = self.api_key

        result = SpeechSynthesizer.call(model=request.model,
                                        text=request.prompt,
                                        sample_rate=48000,
                                        format='wav')
        if result.get_audio_data() is not None:
            with open('output.wav', 'wb') as f:
                f.write(result.get_audio_data())
            playsound('output.wav')
        print(' get response: %s' % (result.get_response()))

        return result.get_response()

    async def audio_sync_to_text(self, data):
        pass

    async def audio_stream_to_text(self, data):
        pass


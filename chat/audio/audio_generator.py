

from chat.audio.factory import AudioGeneratorFactory


class AudioGenerator:
    def __init__(self, model: str):
        self.generator = AudioGeneratorFactory.get_generator(model)

    def text_sync_to_audio(self, text):
        return self.generator.text_sync_to_audio(text)

    def audio_sync_to_text(self, audio):
        return self.generator.audio_sync_to_text(audio)
    def text_stream_to_audio(self, text):
        return self.generator.text_stream_to_audio(text)

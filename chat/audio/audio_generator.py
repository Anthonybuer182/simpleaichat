

from chat.audio.factory import AudioGeneratorFactory


class AudioGenerator:
    def __init__(self, model: str):
        self.generator = AudioGeneratorFactory.get_generator(model)

    def text_sync_to_audio(self, request):
        return self.generator.text_sync_to_audio(request)

    def audio_sync_to_text(self, request):
        return self.generator.audio_sync_to_text(request)
    def audio_stream_to_text(self, task_id):
        return self.generator.audio_stream_to_text(task_id)

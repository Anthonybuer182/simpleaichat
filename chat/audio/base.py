from abc import ABC, abstractmethod

class AudioGeneration(ABC):
    def __init__(self, model):
        self.model = model
    @abstractmethod
    def text_sync_to_audio(self, text):
        pass

    @abstractmethod
    def audio_sync_to_text(self, audio):
        pass

    @abstractmethod
    def text_stream_to_audio(self, text):
        pass

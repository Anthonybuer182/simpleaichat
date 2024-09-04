from abc import ABC, abstractmethod

class AudioGeneration(ABC):
    @abstractmethod
    def text_sync_to_audio(self, text_params):
        pass

    @abstractmethod
    def audio_sync_to_text(self, audio_params):
        pass

    @abstractmethod
    def audio_stream_to_text(self, text_params):
        pass

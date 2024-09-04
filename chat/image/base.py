from abc import ABC, abstractmethod

class ImageGeneration(ABC):
    def __init__(self, model):
        self.model = model
    @abstractmethod
    def text_to_image(self, text):
        pass

    @abstractmethod
    def image_to_image(self, image):
        pass

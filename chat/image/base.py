from abc import ABC, abstractmethod

class ImageGeneration(ABC):
    @abstractmethod
    def text_to_image(self, text_params):
        pass

    @abstractmethod
    def image_to_image(self, image_params):
        pass

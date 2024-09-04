from chat.image.factory import ImageGeneratorFactory

class ImageGenerator:
    def __init__(self, model: str):
        self.generator = ImageGeneratorFactory.get_generator(model)

    def text_to_image(self, text):
        return self.generator.text_to_image(text)

    def image_to_image(self, image):
        return self.generator.image_to_image(image)
    def get_image(self, task_id):
        return self.generator.get_image(task_id)

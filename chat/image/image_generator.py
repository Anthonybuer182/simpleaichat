from chat.image.factory import ImageGeneratorFactory

class ImageGenerator:
    def __init__(self, model: str):
        self.generator = ImageGeneratorFactory.get_generator(model)

    def generate_text_to_image(self, request):
        return self.generator.text_to_image(request)

    def generate_image_to_image(self, request):
        return self.generator.image_to_image(request)
    def get_generate_image(self, task_id):
        return self.generator.get_image(task_id)

from chat.image.flux import FluxGeneration
from chat.image.flux_sdk import FluxGenerationSDK

class ImageGeneratorFactory:
    generators = {
        '': FluxGeneration,
        'flux-schnell':FluxGenerationSDK
    }

    @classmethod
    def get_generator(cls, model):
        for keyword, generator_class in cls.generators.items():
            if model.lower() in keyword.lower():
                return generator_class()
        return FluxGeneration()

from chat.image.flux import FluxGeneration

class ImageGeneratorFactory:
    generators = {
        'flux-schnell': FluxGeneration,
        # 可以在此处添加更多策略
    }

    @classmethod
    def get_generator(cls, model):
        for keyword, generator_class in cls.generators.items():
            if model.lower() in keyword.lower():
                return generator_class()
        raise ValueError(f"No matching model found for '{model}'.")

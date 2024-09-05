

from chat.audio.sambert_sdk import SambertGenerationSDK

class SambertModel:
    def __init__(self,name: str,description: str):
        self.name = name
        self.description = description
class AudioGeneratorFactory:
    generators = {
        SambertGenerationSDK: 
        [
            SambertModel("sambert-zhiqi-v1","温柔女声"),
            SambertModel("sambert-zhixiang-v1","磁性男声"),
        ]
    }

    @classmethod
    def get_generator(cls, model):
        for generator_class, model_list in cls.generators.items():
            for model_object in model_list:
                if model.lower() == model_object.name.lower():
                    return generator_class(model)
        return SambertGenerationSDK("sambert-zhiqi-v1")

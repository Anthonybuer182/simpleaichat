

from chat.audio.sambert_sdk import SambertGenerationSDK

class SambertModel:
    def __init__(self,name: str,description: str):
        self.name = name
        self.description = description
class AudioGeneratorFactory:
    generators = {
        SambertGenerationSDK: 
        [
            SambertModel("sambert-zhixiang-v1","磁性男声"),
            SambertModel("sambert-zhiqi-v1","温柔女声"),
        ],
        SambertModel: 
        [
            SambertModel("sambert-zhixiang-v11","磁性男声"),
            SambertModel("sambert-zhiqi-v11","温柔女声"),
        ]
    }

    @classmethod
    def get_generator(cls, modelName):
        for generator_class, model_list in cls.generators.items():
            for model in model_list:
                if modelName.lower() == model.name.lower():
                    return generator_class()
        return SambertGenerationSDK()

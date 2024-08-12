
import sys
sys.path.append("..")
from simpleaichat.simpleaichat import *

params = {"temperature": 0.7}
model = "qwen-turbo"

ai = AIChat(api_key="sk-1226bc6e75f94b3cba8d8c81dcc8d6f3", console=True, params=params, model=model,character="Elon Musk",character_command="Speak in the style of a Seinfeld monologue")
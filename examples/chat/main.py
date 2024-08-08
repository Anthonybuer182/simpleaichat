
import sys
sys.path.append("..")
from simpleaichat.simpleaichat import *

params = {"temperature": 0.0}
model = "gpt-3.5-turbo-0125"
# AIChat(api_key="sk-1226bc6e75f94b3cba8d8c81dcc8d6f3")
ai = AIChat(api_key="sk-1226bc6e75f94b3cba8d8c81dcc8d6f3", console=True, params=params, model=model)
import sys
sys.path.append("..")
from simpleaichat.simpleaichat import *
# gpt-3.5-turbo-0125
# Ee1imTXK7hDwDM1aFa0337029aD8421bA27882E038CbA163
ai=AIChat(api_key="sk-1226bc6e75f94b3cba8d8c81dcc8d6f3", model="qwen-turbo",console=False)
first = ai("第一款苹果手机叫什么名字")
print("first = " +first)
second = ai("什么时候发布的")
print("second = " +second)
ai.save_session(format="json", minify=True)

# ai=AIChat(api_key="sk-1226bc6e75f94b3cba8d8c81dcc8d6f3", model="qwen-turbo",console=False)
# ai.load_session("chat_session.json",id=ai.get_session().id)
# response = ai("When was it founded?")
# print("second = " +response)
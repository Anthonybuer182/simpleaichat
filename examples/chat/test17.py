import sys
sys.path.append("..")
from simpleaichat.simpleaichat import *
# gpt-3.5-turbo-0125
# Ee1imTXK7hDwDM1aFa0337029aD8421bA27882E038CbA163
json_data={"id":"41efef52-3051-4490-8270-d4684be918dc","created_at":"2024-08-26T02:25:49.547238+00:00","model":"qwen-turbo","system":"You are a helpful assistant.","params":{"temperature":0.7},"messages":[{"role":"user","content":"第一款苹果手机叫什么名字","received_at":"2024-08-26T02:25:49.603797+00:00"},{"role":"assistant","content":"第一款苹果手机的名字叫做iPhone。它于2007年1月9日由史蒂夫·乔布斯正式发布，是苹果公司推出的一款融合音乐播放器、手机和互联网通信设备功能的多用途移动电话。这款产品标志着苹果公司从个人电脑领域向消费电子领域的转型，并对全球智能手机市场产生了深远的影响。","received_at":"2024-08-26T02:25:51.649703+00:00","finish_reason":"stop","prompt_length":26,"completion_length":75,"total_length":101},{"role":"user","content":"什么时候发布的","received_at":"2024-08-26T02:25:51.649860+00:00"},{"role":"assistant","content":"第一款苹果iPhone是在2007年1月9日由史蒂夫·乔布斯正式发布的。","received_at":"2024-08-26T02:25:52.486860+00:00","finish_reason":"stop","prompt_length":113,"completion_length":25,"total_length":138}],"save_messages":True,"total_prompt_length":139,"total_completion_length":100,"total_length":239}
ai=AIChat(console=False)
first=ai.load_json_session(sess_dict=json_data,api_key="sk-1226bc6e75f94b3cba8d8c81dcc8d6f3", model="qwen-turbo")
print("first = ",first)
second = ai("在什么地方发布的?")
print("second = " +second)
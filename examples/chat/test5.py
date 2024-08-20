import sys
sys.path.append("..")
from simpleaichat.simpleaichat import *
# gpt-3.5-turbo-0125
# Ee1imTXK7hDwDM1aFa0337029aD8421bA27882E038CbA163
# ai=AIChat(api_key="sk-Ee1imTXK7hDwDM1aFa0337029aD8421bA27882E038CbA163", model="gpt-3.5-turbo-0125",console=False)
# response = ai("What is the capital of California?")
# print("first = " +response)
# ai.save_session()


json = '{"title": "An array of integers.", "array": [-1, 0, 1]}'
functions = [
             "Format the user-provided JSON as YAML.",
             "Write a limerick based on the user-provided JSON.",
             "Translate the user-provided JSON from English to French."
            ]
params = {"temperature": 0.0, "max_tokens": 100}  # a temperature of 0.0 is deterministic

# We namespace the function by `id` so it doesn't affect other chats.
# Settings set during session creation will apply to all generations from the session,
# but you can change them per-generation, as is the case with the `system` prompt here.
ai=AIChat(api_key="sk-1226bc6e75f94b3cba8d8c81dcc8d6f3", model="qwen-turbo", params=params, save_messages=False,console=False)
for function in functions:
    output = ai(json, ai.get_session().id, system=function)
    print(output)
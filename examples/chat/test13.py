import sys
sys.path.append("..")
from simpleaichat.simpleaichat import *
from pydantic import BaseModel, Field
import orjson
model="qwen-turbo"
api_key= "sk-1226bc6e75f94b3cba8d8c81dcc8d6f3"
params = {"temperature": 0.0}
class write_python_function(BaseModel):
    """Writes a Python function based on the user input."""
    code: str = Field(description="Python code")
    efficient_code: str = Field(description="More efficient Python code than previously written")
ai_struct = AIChat(api_key=api_key, console=False, model=model, params=params, save_messages=False)

response_structured = ai_struct("is_palindrome", output_schema=write_python_function)

# orjson.dumps preserves field order from the ChatGPT API
print(orjson.dumps(response_structured, option=orjson.OPT_INDENT_2).decode())
print("\n\n")
print(response_structured["efficient_code"])
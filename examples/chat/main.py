import sys
sys.path.append("..")
from simpleaichat.simpleaichat import *
from pydantic import BaseModel, Field
from typing import List, Literal, Optional, Union
import orjson
from simpleaichat.simpleaichat.utils import fd
from pydantic import ValidationError
from rich.console import Console
# gpt-3.5-turbo-0125
# Ee1imTXK7hDwDM1aFa0337029aD8421bA27882E038CbA163

AIChat(api_key="sk-1226bc6e75f94b3cba8d8c81dcc8d6f3", model="qwen-turbo")

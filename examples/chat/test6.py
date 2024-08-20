import sys
sys.path.append("..")
from simpleaichat.simpleaichat import *
from pydantic import BaseModel, Field

ai = AIChat(
    console=False,
    save_messages=False,  # with schema I/O, messages are never saved
    model="qwen-turbo",
    api_key="sk-1226bc6e75f94b3cba8d8c81dcc8d6f3",
    params={"temperature": 0.0},
)

class get_event_metadata(BaseModel):
    """Event information"""

    description: str = Field(description="Description of event")
    city: str = Field(description="City where event occured")
    year: int = Field(description="Year when event occured")
    month: str = Field(description="Month when event occured")

# returns a dict, with keys ordered as in the schema
output=ai("First iPhone announcement",id=ai.get_session().id, output_schema=get_event_metadata)
print(output)

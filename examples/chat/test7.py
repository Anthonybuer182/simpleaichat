import sys

sys.path.append("..")
from simpleaichat.simpleaichat import *
from pydantic import BaseModel, Field
from simpleaichat.simpleaichat.utils import wikipedia_search, wikipedia_search_lookup

# This uses the Wikipedia Search API.
# Results from it are nondeterministic, your mileage will vary.
def search(query):
    """Search the internet."""
    wiki_matches = wikipedia_search(query, n=3)
    return {"context": ", ".join(wiki_matches), "titles": wiki_matches}

def lookup(query):
    """Lookup more information about a topic."""
    page = wikipedia_search_lookup(query, sentences=3)
    return page

ai = AIChat(
    console=False,
    model="qwen-turbo",
    api_key="sk-1226bc6e75f94b3cba8d8c81dcc8d6f3",
    params = {"temperature": 0.0, "max_tokens": 100}
)

output=ai("San Francisco tourist attractions", tools=[search, lookup])
print(output)
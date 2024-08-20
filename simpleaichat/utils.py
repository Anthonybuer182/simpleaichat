import os
from typing import List, Union
import logging
import httpx
from pydantic import Field

WIKIPEDIA_API_URL = "https://en.wikipedia.org/w/api.php"


def wikipedia_search(query: str, n: int = 1) -> Union[str, List[str]]:
    SEARCH_PARAMS = {
        "action": "query",
        "list": "search",
        "format": "json",
        "srlimit": n,
        "srsearch": query,
        "srwhat": "text",
        "srprop": "",
    }

    r_search = sync_client().get(WIKIPEDIA_API_URL, params=SEARCH_PARAMS)
    results = [x["title"] for x in r_search.json()["query"]["search"]]

    return results[0] if n == 1 else results


def wikipedia_lookup(query: str, sentences: int = 1) -> str:
    LOOKUP_PARAMS = {
        "action": "query",
        "prop": "extracts",
        "exsentences": sentences,
        "exlimit": "1",
        "explaintext": "1",
        "formatversion": "2",
        "format": "json",
        "titles": query,
    }

    r_lookup = sync_client(proxy=False).get(WIKIPEDIA_API_URL, params=LOOKUP_PARAMS)
    return r_lookup.json()["query"]["pages"][0]["extract"]


def wikipedia_search_lookup(query: str, sentences: int = 1) -> str:
    return wikipedia_lookup(wikipedia_search(query, 1), sentences)


async def wikipedia_search_async(query: str, n: int = 1) -> Union[str, List[str]]:
    SEARCH_PARAMS = {
        "action": "query",
        "list": "search",
        "format": "json",
        "srlimit": n,
        "srsearch": query,
        "srwhat": "text",
        "srprop": "",
    }

    async with async_client() as client:
        r_search = await client.get(WIKIPEDIA_API_URL, params=SEARCH_PARAMS)
    results = [x["title"] for x in r_search.json()["query"]["search"]]

    return results[0] if n == 1 else results


async def wikipedia_lookup_async(query: str, sentences: int = 1) -> str:
    LOOKUP_PARAMS = {
        "action": "query",
        "prop": "extracts",
        "exsentences": sentences,
        "exlimit": "1",
        "explaintext": "1",
        "formatversion": "2",
        "format": "json",
        "titles": query,
    }
    # async with 异步请求需要释放资源
    async with async_client() as client:
        r_lookup = await client.get(WIKIPEDIA_API_URL, params=LOOKUP_PARAMS)
    return r_lookup.json()["query"]["pages"][0]["extract"]


async def wikipedia_search_lookup_async(query: str, sentences: int = 1) -> str:
    return await wikipedia_lookup_async(
        await wikipedia_search_async(query, 1), sentences
    )


def fd(description: str, **kwargs):
    return Field(description=description, **kwargs)


# https://stackoverflow.com/a/58938747
def remove_a_key(d, remove_key):
    if isinstance(d, dict):
        for key in list(d.keys()):
            if key == remove_key:
                del d[key]
            else:
                remove_a_key(d[key], remove_key)

# 设置日志记录器
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    # format="%(asctime)s - %(levelname)s - %(message)s",
    # datefmt="%Y-%m-%d %H:%M:%S"
)

def log_request(request: httpx.Request):
    logger.info("------ Request ------")
    # logger.info(f"Request: {request.method} {request.url}")
    # logger.info(f"Request headers: {request.headers}")
    if request.content:
        logger.info(f"Request body: {request.content.decode().encode('utf-8').decode('unicode_escape')}")
    else:
        logger.info("Request body: No content")

def log_response(response: httpx.Response):
    logger.info("------ Response ------")
    logger.info(f"Response {response.request.method} {response.request.url} - {response.status_code}")
    # logger.info(f"Response headers: {response.headers}")
    if response.stream:
        content = response.read()
    else:
        content = response.text
    body = content.decode(response.encoding or 'utf-8')
    logger.info(f"Response body: {body}")

def sync_client(proxy: bool = True) -> httpx.Client:
    proxies = os.getenv("https_proxy") if proxy else None
    return httpx.Client(
        proxies=proxies,
        event_hooks={
            "request": [log_request],
            "response": [log_response],
        }
    )
def async_client(proxy: bool = True) -> httpx.AsyncClient:
    proxies = os.getenv("https_proxy") if proxy else None
    return httpx.AsyncClient(
        proxies=proxies,
        event_hooks={
            "request": [log_request],
            "response": [log_response],
    })

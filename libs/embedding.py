import logging
import falcon
import os
# from config import EMB_NAME
# from libs.utils import openai_client

from openai import OpenAI
from config import KEY_FILE

def synonyms_normalize(s):
    s = s.replace("台", "臺")
    return s


class OpenAIClient:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with open(KEY_FILE) as fr:
                key = fr.read()
            cls._instance = OpenAI(api_key=key)
        return cls._instance

openai_client = OpenAIClient()
logger = logging.getLogger(__name__)
# OpenAI
KEY_FILE = os.getenv("OPENAI_KEY_FILE", "key.txt")
EMB_NAME = os.getenv("OPENAI_EMB_NAME", "text-embedding-ada-002")
LLM_NAME = os.getenv("OPENAI_LLM_NAME", "gpt-4")
class EmbModelCloud:
    def __init__(self):
        logger.info("Use cloud embedding model")

    def encode(self, text) -> list:
        try:
            response = openai_client.embeddings.create(
                input=text,
                model=EMB_NAME,
            )
            e = response.data[0].embedding
        except Exception as e:
            logger.exception(e)
            raise falcon.HTTPServiceUnavailable("Embedding API is not available.")
        return e

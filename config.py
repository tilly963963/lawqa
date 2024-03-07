import os

KG_FILE = "knowledge/concat_first_second_other_data_20231227_text.pkl"

# OpenAI
KEY_FILE = os.getenv("OPENAI_KEY_FILE", "key.txt")
EMB_NAME = os.getenv("OPENAI_EMB_NAME", "text-embedding-ada-002")
LLM_NAME = os.getenv("OPENAI_LLM_NAME", "gpt-4")

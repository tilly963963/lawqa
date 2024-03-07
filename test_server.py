import os
import logging
import falcon
from web.middleware import LoggingMiddleware
from web.handlers.data_handler import IntentHandler
from web.handlers.file_handler import FileHandler

# from web.handlers.intent_handler import IntentHandler
# from web.handlers.qa_handler import QAHandler
# from libs.vector_search import VectorSearch
# from libs.embedding import EmbModelCloud as EmbModel
# from libs.llm import LLMModelCloud as LLMModel
from libs.parser_html import ParserHtml

import requests

def init_logging():
    formatter = logging.Formatter("%(asctime)s.%(msecs)03d %(levelname)s %(processName)s --- [%(threadName)s] %(name)s : %(message)s", "%Y-%m-%d %H:%M:%S")

    logger_level = int(os.getenv("LOGGER_LEVEL", logging.INFO))
    ch = logging.StreamHandler()
    ch.setLevel(logger_level)
    ch.setFormatter(formatter)

    handlers = [ch]

    logging.basicConfig(level=logger_level, handlers=handlers)


def disable_auto_parse_qs_csv(app):
    app.req_options.auto_parse_qs_csv = False


# init logging system
init_logging()

if __name__ == "__main__":
    pass
    '''
    BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:15009")

    data_1 = {"url":["https://law.moj.gov.tw/Law/LawSearchLaw.aspx?TY=04052005"]}
    res = requests.post(f"{BACKEND_URL}/url", json=data_1).json()

    logging.info("res: {}".format(res))


    data_2 ={"file_data": res["predictions"]}
    res_2 = requests.post(f"{BACKEND_URL}/file", json=data_2).json()
    logging.info("res_2: {}".format(res_2))
    '''

# outs = {
#     "predictions": {},
#     "status": "ok",
# }
# {'高速公路及快速公路交通管制規則': 
#     {'hits': [{'number': ' 第 1 條', 'article': '本規則依道路交通管理處罰條例（以下簡稱本條例）第三十三條第六項規定訂定之。', 'link': 'https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=K0040019', 'meta': {'label': '行政＞交通部＞公路目'}}, 
#             {'number': ' 第 2 條', 'article': '本規則所用名詞，釋

#             ..'}}
#             ]
#     }
# }

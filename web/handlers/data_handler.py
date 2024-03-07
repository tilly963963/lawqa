import os
import json
import time
import logging
import falcon
from dataclasses import asdict
from web.handlers.abstract_handler import AbstractHandler
# from libs.vector_search import VectorSearch
from libs.parser_html import ParserHtml


logger = logging.getLogger(__name__)


class IntentController():
    def __init__(self, **kwargs):
        # self.parser_model = parser_model
        self.parser_model = ParserHtml()
        # self.emb_model = emb_model
        # models = [
        #     VectorSearch(),
        # ]
        # self.models = {m.get_name(): m for m in models}
        # self.algos = list(self.models.keys())
        # logger.info("search engine models: {}".format(self.algos))

    def wrapper(self, results):
        outs = {
            "predictions": {},
            "status": "ok",
        }
        for name, result in results.items():
            outs["predictions"][name] = {
                # "hits": [asdict(r) for r in result["res"]],
                # "time_sec": result["dt"],
                "hits": result
            }
        return outs

    def run(self, urls, **kwargs):
        # query_by = kwargs["query_by"]
        # filter_by = kwargs["filter_by"]
        # institution_by = kwargs["institution_by"]
        # file_by = kwargs["file_by"]

        # t1 = time.time()
        # q_emb = self.emb_model.encode(sentence)
        # qt = round(time.time() - t1, 4)
        import pandas as pd
        urls_data = []
        urls_data={}
        for url in urls:
            parser_url_data = self.parser_model.get_url_data(url)
            # urls_data.extend(parser_url_data)
            urls_data[url]=parser_url_data
        #     for data in parser_url_data: 
        #         page_article_data = self.parser_model.get_article(data)
        #         urls_data.extend(page_article_data)
        # law_link_df = pd.DataFrame(urls_data)
        # law_link_df.to_csv('urls_data.csv', encoding="utf-8-sig")

        result = self.wrapper(urls_data)
        # logger.info("result: {}".format(result))

        return result

class IntentHandler(AbstractHandler):
    handler_identifier = "data_index"

    def __init__(self, **kwargs):
        
        self.controller = IntentController(**kwargs)

        # pick anyone. Every model should use the same knowledge.
        # key = list(self.controller.models.keys())[0]
        # df = self.controller.models[key].df
        # sub_df = df[df["institution"] != "其他機關"]
        # data = []
        # for _, row in sub_df.drop_duplicates(["filename"]).iterrows():
        #     data.append({
        #         "filename": row["filename"],
        #         "institution": row["institution"],
        #         "labels": row["label"].split(","),
        #     })
        # self.kg_files = data

    # def _on_get(self, req, res):
        # sentence = req.get_param("sentence", required=True)
        # logger.info("sentence: {}".format(sentence))
        # query_by = req.get_param("query_by", [])
        # filter_by = req.get_param("filter_by", [])
        # institution_by = req.get_param("institution_by", [])
        # file_by = req.get_param("file_by", [])

        # if sentence == "":
        #     raise falcon.HTTPBadRequest("sentence is required")

        # args = {"query_by": query_by, "filter_by": filter_by, "institution_by": institution_by,"file_by":file_by}
        # return self.controller.run(sentence, **args)

    def _on_post(self, req, res):
        # logger.info("event: on_post, data: {}".format(req.context["data"]))
        logger.info("event: on_post, data")

        ## 取出所有參數
        # 用戶輸入的搜尋句
        urls = req.context["data"].get("url", "")
        # 要搜尋的欄位，預設搜尋段落
        # query_by = req.context["data"].get("query_by", ["text"])
        # # 指定的類別
        # filter_by = req.context["data"].get("filter_by", [])
        # # 指定主管機關
        # institution_by = req.context["data"].get("institution_by", [])

        # file_by = req.context["data"].get("file_by", [])

        if urls == "":
            raise falcon.HTTPBadRequest("sentence is required")

        return self.controller.run(
            urls,
            # query_by=query_by,
            # filter_by=filter_by,
            # institution_by=institution_by,
            # file_by=file_by
        )

    # def on_get_algo(self, req, res):
    #     result = self.controller.algos
    #     result = json.dumps(result, ensure_ascii=False, sort_keys=True)
    #     res.body = result
    #     res.status = falcon.HTTP_200

    # def on_get_kg_file(self, req, res):
    #     output = {
    #         "file": self.kg_files,
    #         "status": "ok",
    #     }
    #     output = json.dumps(output, ensure_ascii=False, sort_keys=True)
    #     res.body = output
    #     res.status = falcon.HTTP_200

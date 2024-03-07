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


class FileController():
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
               "hits":  result
            }
        return outs

    def run(self, file_data, **kwargs):
        # query_by = kwargs["query_by"]
        # filter_by = kwargs["filter_by"]
        # institution_by = kwargs["institution_by"]
        # file_by = kwargs["file_by"]

        # t1 = time.time()
        # q_emb = self.emb_model.encode(sentence)
        # qt = round(time.time() - t1, 4)
        import pandas as pd

        article_datas={}
        law_datas={}
        num=0
        for url, datas in file_data.items(): 
            for file_name, data in datas['hits'].items(): 
                # if isinstance (data['link'],str) :
                    
                    article_data = self.parser_model.get_article(file_name, data)
                    article_datas[file_name]=article_data
        logger.info("!!article_datas: {}".format(article_datas))

        for k,v in article_datas.items():
            for data in v:
                num=num+1
                law_datas[num]=data


        law_link_df = pd.DataFrame(law_datas).T
        law_link_df.to_csv('law.csv', encoding="utf-8-sig")

        result = self.wrapper(article_datas)
        logger.info("result: {}".format(result))

        return result

class FileHandler(AbstractHandler):
    handler_identifier = "data_index"

    def __init__(self, **kwargs):
        
        self.controller = FileController(**kwargs)

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
        logger.info("event: on_post, data ")

        # logger.info("event: on_post, data: {}".format(req.context["data"]))

        ## 取出所有參數
        # 用戶輸入的搜尋句
        file_data = req.context["data"].get("file_data", "")
        # 要搜尋的欄位，預設搜尋段落
        # query_by = req.context["data"].get("query_by", ["text"])
        # # 指定的類別
        # filter_by = req.context["data"].get("filter_by", [])
        # # 指定主管機關
        # institution_by = req.context["data"].get("institution_by", [])

        # file_by = req.context["data"].get("file_by", [])

        if file_data == "":
            raise falcon.HTTPBadRequest("sentence is required")

        return self.controller.run(
            file_data,
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
'''
    input_url = st.text_input(
        "輸入url", placeholder=""
    )
    st.write('https://law.moj.gov.tw/Law/LawSearchLaw.aspx?TY=04052005')


    if input_url:
        st.markdown('----')
        url_data = {"url":[input_url]}
        res = requests.post(f"{BACKEND_URL}/url", json=url_data).json()
        # st.write(res)
        article_datas={}
        file_names=[]
        for url, datas in res["predictions"].items(): 
            for file_name, data in datas['hits'].items(): 
                file_names.append(file_name)
        select = st.multiselect(
            "URL FILE 👇",
            options=file_names, 
            default=file_names
            # disabled=st.session_state.get("clicked"),
            # horizontal=True,
        )
    # add_selectbox = st.sidebar.selectbox(
    #     "How would you like to be contacted?",
    #     ("Email", "Home phone", "Mobile phone")
    # )
'''

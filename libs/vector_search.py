import os
import json
import logging
import pandas as pd
from typing import List

# from libs.abstract_search import AbstractSearch, SearchResult

try:
    import chromadb
except RuntimeError:
    import sys
    import pysqlite3
    sys.modules["sqlite3"] = sys.modules["pysqlite3"]
    import chromadb


logger = logging.getLogger(__name__)

VECTOR_DB_NAME = "pycon_law_rag"
DIST_TYPE = "cosine"
DIST_THRESHOLD = float(os.getenv("DIST_THRESHOLD", 0.2))
from dataclasses import dataclass, field
from typing import List


@dataclass
class SearchResult:
    """
    required: index, filename, text, query
    """
    index: int  # index in source dataframe
    filename: str
    text: str    # 段落文本內容
    query: str   # origin query
    source: str = ""  # 條目
    # page: int = -1    # 頁數
    dist: float = -1  # search distance / score
    meta: dict = field(default_factory=lambda : {})  # meta data，其餘想放的資訊

class AbstractSearch:
    def need_emb(self) -> bool:
        # 是否為需要embedding的演算法
        raise falcon.HTTPNotFound(title="need_emb() not implemented")

    def get_name(self) -> str:
        # 回傳該方法的名稱
        raise falcon.HTTPNotFound(title="get_name() not implemented")

    def query(self, sentence: str, **kwargs) -> List[SearchResult]:
        raise falcon.HTTPNotFound(title="query() not implemented")
class VectorSearch(AbstractSearch):
    def __init__(self):
        KG_FILE = './law.csv'
        logger.info("Build knowledge...from {}".format(KG_FILE))

        # load data
        self.df = pd.read_csv(KG_FILE)
        self.df.reset_index(drop=True, inplace=True)

        logger.info(f"knowledge data shape: {self.df.shape}")

        # build vector db
        db_client = chromadb.Client()
        try:
            db_client.delete_collection(VECTOR_DB_NAME)
        except:
            pass
        self.collection = db_client.create_collection(
            VECTOR_DB_NAME,
            {
                "hnsw:space": DIST_TYPE,
                "hnsw:construction_ef": 100,
                "hnsw:M": 32
            }
        )

        ids = [str(i) for i in range(self.df.shape[0])]
        docs = self.df["article"].tolist()
        embs = self.df["article_emb"].tolist()
        metas = self.df["meta"].tolist()
        try:
            self.collection.add(
                ids=ids,
                documents=docs,
                embeddings=embs,
                metadatas=metas
            )
        except Exception as e:
            logger.exception(e)
            raise

        logger.info("Finished building knowledge!")

    def get_text(self, idx):
        if idx >= len(self.df) or idx < 0:
            falcon.HTTPBadRequest("snippets value not valid")

        return self.df.iloc[idx]["article"]

    def need_emb(self):
        return True

    def get_name(self):
        return "語意搜尋"

    def search(self, sentence, **kwargs) -> List[SearchResult]:
        # 不支援搜尋檔名，因為現在只有對內文建立embedding
        label_by = kwargs["label_by"] # list
        file_by = kwargs["file_by"] # list
        query_emb = kwargs["q_emb"] # list

        results = self.collection.query(
            query_embeddings=query_emb,
            n_results=100,
        )
        ids = results["ids"][0]
        dists = results["distances"][0]

        outputs = []
        # if (file_by == []) & (filter_by is None) & (institution_by is None):
        #     return outputs
        for i in range(len(ids)):
            if dists[i] >= DIST_THRESHOLD:
                break
            idx = int(ids[i])
            row = self.df.iloc[idx]
            df_label = row["meta"]["label"] 
            logger.info("df_label {}".format(df_label))

            if file_by:
                if row["filename"] not in file_by:
                    continue
            else:
                if label_by:
                    if df_label not in label_by:
                        continue
            r = SearchResult(
                index=idx,
                filename=row["filename"],
                text=row["article"],
                query=sentence,
                source=row["num"],
                meta={"labels":list(row["labels"])},
                # page=row["page"],
                dist=dists[i],
            )
            outputs.append(r)
        return outputs


# if __name__ == "__main__":
#     search_engine = VectorSearch()
#     sentence = '酒駕罰多少錢'
#     file_by=[]
#     label_by = ['']
#     search_engine.search()


import os
import json
import logging
import numpy as np
import pandas as pd
from dataclasses import dataclass
from typing import List

import requests
from bs4 import BeautifulSoup
from libs.embedding import EmbModelCloud

logger = logging.getLogger(__name__)

class ParserHtml:
    def __init__(self):
        self.emb_model = EmbModelCloud()

    def get_url_data(self, root_url):
        title_link = []
        prefix_url = 'https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode='

        try:
            r = requests.get(root_url) #將此頁面的HTML GET下來

            soup = BeautifulSoup(r.text,"html.parser")

            rule = soup.find("div", {'class': 'law-result'})
            rule = rule.text.replace(' ','').replace('\n','').replace('\r','')
            label = rule.split('＞')[-1]
            table = soup.find("table", {'class': 'table table-hover tab-list tab-central'})

            data={}
            for row in table.tbody.find_all('tr'):
                columns = row.find_all('td')
                raw_link = columns[2].a['href']
                # logger.info("title: {}".format(columns[2].a['title']))
  
                PCode = raw_link.split("?PCode=")[1]

                link = prefix_url + PCode
        
                # data = {'file': columns[2].a['title'] , 'link':link, 'raw_link': raw_link, 'meta':{'label':rule}}
                data[columns[2].a['title']]= {'file': columns[2].a['title'],'link':link, 'raw_link': raw_link, 'meta':{'label':label}}
                
                # title_link.append(data)

        except requests.exceptions.RequestException as e:
            print(e)

        return data

    def get_article(self,file_name, data):
        try:
            r = requests.get(data["link"])
            soup = BeautifulSoup(r.text, 'html.parser')

            results = soup.find('div', attrs={'class':'law-reg-content'})

            save_data = []
            for result in results.find_all('div', attrs={'class':'row'}):
                number = result.find('div', attrs={'class':'col-no'}).text
                article = result.find('div', attrs={'class':'law-article'}).text.replace('\n','')
                article_emb = self.emb_model.encode(article)
                data = {'file_name':file_name ,'number':number, 'article':article ,'article_emb':article_emb, 'link':data["link"], 'meta':data["meta"]}
                save_data.append(data)
        except requests.exceptions.RequestException as e:
            print(e)
        
        return save_data

      
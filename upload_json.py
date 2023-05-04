import json

"""To ingest data in Elastic Search"""

import os
import pandas as pd
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from sentence_transformers import SentenceTransformer
# from config.__init___ import DATA_CONFIGURATION


# # the path to the file containing the data to be ingested

ES_INDEX_FILE = "C:/Users/Acer/Desktop/IIL/IIL_data/"

ES_HOST = 'localhost'
ES_PORT = 9200

# the name of the Elasticsearch index where the data will be ingested
ES_INDEX = "sample"
ES_EMB_MODEL = 'nli-bert-base'

# model = SentenceTransformer('nli-bert-base')
model = SentenceTransformer(ES_EMB_MODEL)

client = Elasticsearch([{ 'scheme':'http', 'host': 'localhost', 'port': 9200}])
# client.indices.create(index= "new_index")

print(client.ping())

def getkg(filepath):
    docs = []
    fpath = filepath
    for i in range(1,6):
        filepath = fpath + str(i) + ".json"
        # print(filepath)
        with open(filepath, 'r') as f:
            data = json.load(f)
        for record in data:
            # print(record)
            # print(type(record))
            doc = {
                "Description": record.get("Description"),
                "Service and Maintenance": record.get("Service and Maintenance"),
                "Causes for anomaly" : record.get("Causes for anomaly"),
                "Role" : record.get("Role"),
                "Root Causes": record.get("Root Causes"),
                "Recommendations for Solution": record.get("Recommendations for Solution"),
                "Preventive Actions": record.get("Preventive Actions"),
                "Corrective Actions": record.get("Corrective Actions")
            }
            docs.append(doc)
            # print(docs)
    return docs



def ingest_data_embedding(index_name):
        if index_name == "":
            INDEX_NAME = ES_INDEX
        else:
            INDEX_NAME = index_name
        
        # deleting index with the same name.

        client.indices.delete(index=INDEX_NAME, ignore=[404])
        
        source = {
            "settings": {
                "number_of_shards": 2,
                "number_of_replicas": 1,
                "elastiknn": True,
                "index.max_ngram_diff": 10,
                "analysis": {
                    "analyzer": {
                        "ngram_analyzer": {
                            "tokenizer": "ngram_tokenizer",
                            "filter": ["lowercase"]
                        }
                    },
                    "tokenizer": {
                        "ngram_tokenizer": {
                            "type": "ngram",
                            "min_gram": 3,
                            "max_gram": 10,
                            "token_chars": ["letter", "digit"]
                        }
                    }
                }
            },
            "mappings": {
                "properties": {
                   
                }   
            }
        }


        client.indices.create(index=INDEX_NAME, body=source, ignore=400)

        kg = getkg(DATA_FILE)
        print(kg)
        requests = []
        for i, node in enumerate(kg):
            request = node
            request["_op_type"] = "index"
            request["_index"] = INDEX_NAME
            requests.append(request)
        bulk(client, requests)
        client.indices.refresh(index=INDEX_NAME)
        return 1



kg = getkg(ES_INDEX_FILE)
INDEX_NAME = "new4"
DATA_FILE = ES_INDEX_FILE

ingest_data_embedding(INDEX_NAME)








# def getkg(filepath):
#     df = pd.read_csv(filepath)
#     df = df.dropna(axis=0)
#     docs = []
#     for row in df.iterrows():
#         series = row[1]
#         print(series)
#         doc = {
#             "Description": series.Description,
#             "Causes": series.Causes,
#             "Solution": series.Solution
#         }
#         docs.append(doc)
#     print(docs)
#     return docs





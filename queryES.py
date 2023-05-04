from elasticsearch import Elasticsearch

# create a connection to Elasticsearch
client = Elasticsearch([{ 'scheme':'http', 'host': 'localhost', 'port': 9200}])

print(client.ping())

search_body = {
    "query": {
        "match": {
            "Root Causes": "Refrigerant Leaks"
        }
    }
}

# search for documents in an index
results = client.search(index='new3', body=search_body)

# print the search results
for hit in results['hits']['hits']:
    print("Score:", hit['_score'])
    print(hit['_source']['Description'], hit['_source']['Root Causes'])
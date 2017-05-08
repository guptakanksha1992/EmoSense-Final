# This is the file where we connect to ES + find and insert data

from elasticsearch import Elasticsearch, RequestsHttpConnection
import ConfigParser

# Our elastic search engine
config = ConfigParser.ConfigParser()
config.readfp(open(r'./configurations.txt'))

HOST = config.get('ES Instance', 'elastic_search_host_address')
PORT = config.get('ES Instance', 'Port')

class ElasticSearchServices:

    def __init__(self):
        self.es = Elasticsearch(
            hosts=[{'host': HOST, 'port': 443}],
            use_ssl=True,
        )

    def store_data(self, index, doc_type, body):
        results = self.es.index(
    			index=index,
    			doc_type=doc_type,
    			body=body
    		)

        return results

    def create_collection(self, index, body):
        print "Creating collection with index:", index
        results = self.es.indices.create(
            index=index,
            ignore=400,
            body=body
        )
        return results

    def search(self, index, doc_type, body, size):
    	results = self.es.search(
    			index = index,
    			doc_type = doc_type,
    			body = body,
    			size = size
    		)

    	return results

    def total_hits(results):
    	return results['hits']['total']
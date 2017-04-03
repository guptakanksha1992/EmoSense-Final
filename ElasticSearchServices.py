# This is the file where we connect to ES + find and insert data

from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

# Our elastic search engine
#awsauth = AWS4Auth('AKIAINYR7GOTUOL4IWUQ', 'E4yhGRR4QBGlLKLMAy/DEpYy5zqq9QMN54uN050q', "us-west-1", 'es')
HOSTADDRESS='search-tweetmap-whpei25apwtxe7bvkmaj34ozee.us-west-1.es.amazonaws.com'
#awsauth = AWS4Auth('AKIAINHSJW74HQTPGTYQ', 'ROcOAC4P3iJ4pkX1ySJjDNJfvTzmLFFqAcE7XW3l', "us-west-1", 'es')
awsauth = AWS4Auth('AKIAINYR7GOTUOL4IWUQ', 'E4yhGRR4QBGlLKLMAy/DEpYy5zqq9QMN54uN050q', "us-west-1", 'es')

class ElasticSearchServices:

    def __init__(self):
        self.es = Elasticsearch(
            hosts=[{'host': HOSTADDRESS, 'port': 443}],
            http_auth=awsauth,
            use_ssl=True,
            verify_certs=True,
            connection_class=RequestsHttpConnection
        )

    def store_data(self, index, doc_type, body):
        results = self.es.index(
    			index=index,
    			doc_type=doc_type,
    			body=body
    		)

        return results

    def create_collection(self, index, body):
        print ("Creating collection...")
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


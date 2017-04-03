# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 19:42:02 2017

@author: Sarang
"""


from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

HOSTADDRESS='search-tweetmap-whpei25apwtxe7bvkmaj34ozee.us-west-1.es.amazonaws.com'
awsauth = AWS4Auth('AKIAINHSJW74HQTPGTYQ', 'ROcOAC4P3iJ4pkX1ySJjDNJfvTzmLFFqAcE7XW3l', "us-west-1", 'es')

# Our elastic search engine

es = Elasticsearch(
    hosts=[{'host': HOSTADDRESS, 'port': 443}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)
print(es.info())

index = "finaltwittermapindex5"
doc_type = "finaltweets2"
keyword =  'Food'


collection = {
	"mappings": {
		"finaltweets2": {
			"properties": {
				"id": {
					"type": "string"
				},
				"message": {
					"type": "string"
				},
				"author": {
					"type": "string"
				},
				"timestamp": {
					"type": "string"
				},
				"location": {
					"type": "geo_point"
				}
			}
		}
	}
}


search_body = {
			"query": {
				"match": {
					"_all": keyword
				}
			}
		}

size = 10000

distance_string = '200'
latitude = '40.17887331434696'
longitude = '-86.572265625'

body = {
			"query": {
				"match": {
					"_all": keyword
				}
			},
			"filter": {
				"geo_distance": {
					"distance": distance_string,
					"distance_type": "sloppy_arc",
					"location": {
						"lat": latitude,
						"lon": longitude
					}
				}
			}
		}

size = 10000
result = es.search(index, body)

print result

'''

print es.indices.create(
            index=index,
            ignore=400,
            body=collection
        )
        
        
        
print "Saving Sample tweet"
id='1'
tweet='Hello, world!'
author='Sarang'
timestamp=
location_data[0]
location_data[1]
body = {
			"id": id,
			"message": tweet,
			"author": author,
			"timestamp": timestamp,
			"location": location_data
		}

		result = self.es.store_data(self.index, self.doc_type, body)

result =  es.search(
    			index = index,
    			doc_type = doc_type,
    			body = search_body,
    			size = size
    		)


print result       


    es.index(
    			index=index,
    			doc_type=doc_type,
    			body=body
    		)
      '''

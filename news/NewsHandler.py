from ElasticSearchServices import ElasticSearchServices

class NewsHandler:

	def __init__(self):
		self.es = ElasticSearchServices()
		self.index = "news2"
		self.doc_type = "article"

	def getNews(self, keyword):
		body = {
			"query": {
				"match": {
					"_all": keyword
				}
			}
		}

		size = 10000
		result = self.es.search(self.index, self.doc_type, body, size)

		return result

	def getNewsArticles(self, keyword, distance, latitude, longitude):
		distance_string = distance + 'km'
		if (type(latitude) != float):
			latitude = float(latitude)

		if (type(longitude) != float):
			longitude = float(longitude)

		body = 	{
				    "query": {
				        "bool": {
				            "must": {
				                "match": {"_all": keyword }
				            },
				        	"filter": {
								"geo_distance": {
									"distance": distance_string,
									#"distance_type": "sloppy_arc",
									"location": {
										"lat": latitude,
										"lon": longitude
									}
								}
							}
					    }
				    }
				}

		size = 10000
		result = self.es.search(self.index, self.doc_type, body, size)

		return result

	def getNewsWithDistance(self, latitude, longitude, t_start, t_end, max_emotion)
		distance=1000
		distance_string = distance + 'km'
		print ('Searching ', distance_string, ' from location Latitude: ', latitude, ' ; Longitude: ', longitude)

		if (type(latitude) != float):
			latitude = float(latitude)

		if (type(longitude) != float):
			longitude = float(longitude)

		body = 	{
    "query":{
                "bool" : {
                    "must" : [
                        {"match":{"dominant_emotion":max_emotion}}
                        ],
                    "must_not":
                        {"range": {
                    "timestamp":{
                        "gte": t_end,
                        "lte": t_start
                    }
                 }
                },
            "filter":{
            "geo_distance" : {
                "distance" : distance_string,
                "location" : {
                    "lat" : latitude,
                    "lon" : longitude
                }
            }
        }

        }
    }
}

		size = 10000
		result = self.es.search(self.index, self.doc_type, body, size)

		return result

	def insertNews(self, title, author, url, url2image, source, timestamp, location_data, sentiment,dominant_emotion, anger, joy, sadness, fear, disgust ):

		body = {
			"title": title,
			"author": author,
			"url": url,
			"url2image": url2image,
			"source": source,
			"timestamp": timestamp,
			"location": location_data,
			"sentiment": sentiment,
			"dominant_emotion":dominant_emotion,
			"anger": anger,
			"joy":joy,
			"sadness":sadness,
			"fear": fear,
			"disgust": disgust
		}

		print 'Inserting the following body:'
		print body
		print 'In index:', self.index, 'and document:', self.doc_type

		result = self.es.store_data(self.index, self.doc_type, body)

		return result

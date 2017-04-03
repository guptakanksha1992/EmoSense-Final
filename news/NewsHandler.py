from ElasticSearchServices import ElasticSearchServices

class NewsHandler:

	def __init__(self):
		self.es = ElasticSearchServices()
		self.index = "news"
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

	def getNewsArticles(self, keyword, time, latitude, longitude):
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

	def insertNews(self, title, author, url, url2image, source, timestamp, location_data):

		body = {
			"title": title,
			"author": author,
			"url": url,
			"url2image": url2image,
			"source": source,
			"timestamp": timestamp,
			"location": location_dataa
		}

		result = self.es.store_data(self.index, self.doc_type, body)

		return result


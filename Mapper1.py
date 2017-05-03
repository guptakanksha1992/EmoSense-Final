# Here is where we can  search for news from the ES based on time, location and dominant emotion

from ElasticSearchServices import ElasticSearchServices

class NewsSearchHandler:

	def __init__(self):
		self.es = ElasticSearchServices()
		self.index = "news2"
		self.doc_type = "article"


	def getNewsWithDistance(self,  latitude, longitude, startTime, EndTime, dominantEmotion):
		distance=1000;
		distance_string = distance + 'km'
		print ('Searching ', distance_string, ' from location Latitude: ', latitude, ' ; Longitude: ', longitude)

		if (type(latitude) != float):
			latitude = float(latitude)

		if (type(longitude) != float):
			longitude = float(longitude)

		body = 	{
            "query": {
                "match_all": {},
                 "range": {
                    "timestamp": {
                        "gte": startTime,
                        "lte": EndTime
                    }
                }
            }        ,
				        	"filter": {
								"geo_distance": {
									"distance": distance_string,
									#"distance_type": "sloppy_arc",
									"location": {
										"lat": latitude,
										"lon": longitude
									}

								},
                                "dominant_emotion": dominantEmotion
							}
					    }


		size = 10000
		result = self.es.search(self.index, self.doc_type, body, size)
		return result




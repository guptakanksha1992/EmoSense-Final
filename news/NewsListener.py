import json
from NewsHandler import NewsHandler
from ElasticSearchServices import ElasticSearchServices
import random
import requests

REQUEST_LIMIT = 420

#---- Elastic Search Details -------

index = "news"
collection = {
	"mappings": {
		"article": {
			"properties": {
				"title": {
					"type": "string"
				},
				"author": {
					"type": "string"
				},
                "url": {
                    "type": "string"
                },
                "url2image": {
                    "type": "string"
                },
				"source": {
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


#--------------------------------------------------------


try:
    collection_service = ElasticSearchServices()
    collection_service.create_collection(index, collection)
except:
    print "Index already created"

class NewsListener(StreamListener):

    def on_data(self, data):
        try:
            parse_data(data)
        except:
            # print(data)
            print("No location data found")

        return(True)

    def on_error(self, status):
        errorMessage = "Error - Status code " + str(status)
        print(errorMessage)
        if status == REQUEST_LIMIT:
            print("Request limit reached. Trying again...")
            exit()

    def parse_data(data):
        json_data_file = json.loads(data)
        tweetHandler = TwitterHandler()

        location = json_data_file["place"]
        coordinates = json_data_file["coordinates"]

        if coordinates is not None:
            # print(json_data_file["coordinates"])
            final_longitude = json_data_file["coordinates"][0]
            final_latitude = json_data_file["coordinates"][0]
        elif location is not None:
            coord_array = json_data_file["place"]["bounding_box"]["coordinates"][0]
            longitude = 0;
            latitude = 0;
            for object in coord_array:
                longitude = longitude + object[0]
                latitude = latitude + object[1]


            final_longitude = longitude / len(coord_array)
            final_latitude = latitude / len(coord_array)
        else:

        	# Insert code for random final_longitude, final_latitude here

            final_longitude=random.uniform(-180.0,180.0)
            final_latitude=random.uniform(-90.0, +90.0)
            
        tweetId = json_data_file['id_str']
        tweet = json_data_file["text"]
        author = json_data_file["user"]["name"]
        timestamp = json_data_file["created_at"]

        location_data = [final_longitude, final_latitude]
        try:
            print(tweetHandler.insertTweet(tweetId, location_data, tweet, author, timestamp))
        except:
            print("Failed to insert tweet")

    def startStream():

        auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
        auth.set_access_token(accessToken, accessSecret)
        while True:
            try:
                twitterStream = Stream(auth, TweetListener())
                twitterStream.filter(track=KEYWORDS)
            except:
                print("Restarting Stream")
                continue
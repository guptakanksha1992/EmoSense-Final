from ElasticSearchServices import ElasticSearchServices
from TweetHandler import TwitterHandler
import json

# ---- Elastic Search Details -------

index = "newsdomain"
collection = {
	"mappings": {
		"finaltweets2": {
			"properties": {
				"id": {
					"type": "string"
				},
                "source": {
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
				},
                "sentiment": {
					"type": "string"
				},
                "anger": {
					"type": "float"
				},
                "joy": {
					"type": "float"
				},
                "sadness": {
					"type": "float"
				},
                "fear": {
					"type": "float"
				},
                "disgust": {
					"type": "float"
				}
			}
		}
	}
}

# --------------------------------------------------------

try:
    collection_service = ElasticSearchServices()
    collection_service.create_collection(index, collection)
except:
    print "Index already created!!"


def persistTweet(tweet):
    print "Tweet received by persister: ", tweet
    tweeter = TwitterHandler()
    json_msg = json.loads(tweet['Message'])
    tid = json_msg['id']
    location_data = json_msg['location']
    message = json_msg['message']
    author = json_msg['author']
    timestamp = json_msg['timestamp']
    sentiment = json_msg['sentiment']
    anger = json_msg['anger']
    joy = json_msg['joy']
    sadness = json_msg['sadness']
    fear = json_msg['fear']
    disgust = json_msg['disgust']

    response = tweeter.insertTweet(tid, location_data, message, author, timestamp, sentiment, anger,joy,sadness,fear,disgust)
    # print response
    return response
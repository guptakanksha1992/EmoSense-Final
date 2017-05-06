import tweepy
from tweepy import Stream
import ConfigParser
from tweepy.streaming import StreamListener
from TweetHandler import TwitterHandler
from ElasticSearchServices import ElasticSearchServices
import random
import json


#----------SQS & SNS Details---------------------------
import boto.sns
import boto.sqs
from boto.sqs.message import Message
#----------Sentiment Analysis methods------------------

from sentiment_analysis import *


reload(sys)
sys.setdefaultencoding('utf8')

config = ConfigParser.ConfigParser()
config.readfp(open(r'./configurations.txt'))

HOST = config.get('ES Instance', 'elastic_search_host_address')
PORT = config.get('ES Instance', 'Port')

#consumer key, consumer secret, access token, access secret.
consumerKey = config.get('Twitter API Keys', 'ConsumerKey')
consumerSecret = config.get('Twitter API Keys', 'ConsumerSecret')
accessToken = config.get('Twitter API Keys', 'AccessToken')
accessSecret = config.get('Twitter API Keys', 'AccessSecret')
aws_api_key = config.get('AWS Keys', 'aws_api_key')
aws_secret = config.get('AWS Keys', 'aws_secret')

KEYWORDS = ['Sports', 'Politics', 'Technology', 'Health', 'Entertainment','Apple','IBM','Sony','Maggi']
REQUEST_LIMIT = 420

#---- Elastic Search Details -------

index = "newsdomain3"
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

#--------------------------------------------------------

class TweetListener(StreamListener):

    def on_data(self, data):
        try:
            parse_data(data)
        except Exception as e:
            print("Parsing Error " + str(e))
        try:
            elastic_worker_sentiment_analysis()
        except Exception as e:
            print("Elastic work sentiment Error " + str(e))

        return (True)

    def on_error(self, status):
        errorMessage = "Error - Status code " + str(status)
        print(errorMessage)
        if status == REQUEST_LIMIT:
            print("Request limit reached. Trying again...")
            exit()

def formatTweet(id, location_data, tweet, author, timestamp):
    tweet = {
        "id": id,
        "message": tweet,
        "author": author,
        "timestamp": timestamp,
        "location": location_data
    }
    return tweet


def parse_data(data):
    try:
        json_data_file = json.loads(data)
    except Exception as e:
        print ('Parsing failed')
        print (str(e))
    # Could be that json.loads has failed

    # print 'JSON DATA FILE:', json_data_file

    try:
        location = json_data_file["place"]
        coordinates = json_data_file["coordinates"]
    except Exception as e:
        print ('Location data parsing erroneous')
        print (str(e))

    # Setting location of the tweet

    if coordinates is not None:
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
        return

    tweetId = json_data_file['id_str']
    tweet = json_data_file["text"]
    author = json_data_file["user"]["name"]
    timestamp = json_data_file["created_at"]
    location_data = [final_longitude, final_latitude]
    # Tweet ready (without sentiment analysis by this point) - sending to queue
    # print tweetId, location_data, tweet, author, timestamp

    try:
        # Format tweet into correct message format for SQS
        formatted_tweet = formatTweet(tweetId, location_data, tweet, author, timestamp)
        tweet = json.dumps(formatted_tweet)

        # print 'Trying to publish to Queue the tweet', tweet
        publishToQueue(tweet)

    except Exception as e:
        print("Failed to insert tweet into SQS")
        #print str(e)

def publishToQueue(tweet):
    try:

        # Establishing Connection to SQS
        conn = boto.sqs.connect_to_region("us-east-1", aws_access_key_id=aws_api_key,
                                          aws_secret_access_key=aws_secret)
        #print "Connected to SQS!!"
        # print "Tweet is :", tweet
        # print "All queues:", conn.get_all_queues()
        # q = conn.create_queue('Trial2')
        q = conn.get_queue('EmoSense_Queue')  # Connecting to the SQS Queue named tweet_queue
        #print "Connected to queue!!"
        m = Message()  # Creating a message Object

        m.set_body(tweet)
        q.write(m)
        #  print 'Added to Queue'
    except Exception as e:
        print ('Failed to publish to Queue')
        print (str(e))

def elastic_worker_sentiment_analysis():
    # This method acts as an Elastic BeanStalk worker

    # Receiving the message from SQS
    '''print 'Fetching from SQS and publishing to SNS'
                print '---------------------------------------'''
    try:
        conn = boto.sqs.connect_to_region("us-east-1",  aws_access_key_id=aws_api_key,
                                      aws_secret_access_key=aws_secret)
        q = conn.get_queue('EmoSense_Queue')

        # Storing the result set
        rs = q.get_messages()

        # Extracting the message from resultset
        m = rs[0]

        # Extracting tweet from message
        tweet = m.get_body()

        sentiment, anger, joy, sadness, fear, disgust = tweet_sentiment_analysis(tweet)
        print ("Before SNS: ", tweet)


        # SNS Connection

        conn = boto.sns.connect_to_region('us-east-1', aws_access_key_id=aws_api_key,
                                      aws_secret_access_key=aws_secret)
        topic = 'arn:aws:sns:us-east-1:836578494369:EmoSense_topic'

        # Appending sentiment data to JSON Format of the message tweet

        message_json = json.loads(tweet)
        # print 'Message_json', message_json
        message_json['sentiment'] = sentiment
        message_json['anger'] = anger
        message_json['joy'] = joy
        message_json['sadness'] = sadness
        message_json['fear'] = fear
        message_json['disgust'] = disgust
        print ("Before SNS: ", message_json)
        # Publishing to SNS
        conn.publish(topic=topic, message=json.dumps(message_json), message_structure=json)
        print ("Published to SNS")
    except Exception as e:
        print ('Exception ' + str(e))


def startStream():
    auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
    auth.set_access_token(accessToken, accessSecret)
    while True:
        try:
            twitterStream = Stream(auth, TweetListener())
            twitterStream.filter(languages=['en'], track=KEYWORDS)
        except Exception as e:
            print("Restarting Stream", str(e))
            continue

    #The location specified above gets all tweets, we can then filter and store based on what we want

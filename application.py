import json
import thread
import time
import requests
import threading

from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, send, emit

from TweetListener import startStream
from TweetHandler import TwitterHandler
import TweetPersister
#----------------------------------------

# News Fetching and Handling API
from news import NewsHandler
from news.NewsListener import *
#----------------------------------------

# Graph Populating code
from GraphHandler import *
#----------------------------------------

# Config parsers
import ConfigParser


# Function that checks if a keyword exists in the Config file, and appends a record if it doesn't
def configChanger(keyword):
    config = ConfigParser.ConfigParser()
    config.readfp(open(r'./configurations.txt'))
    KEYWORDS = config.get('Keywords', 'twitter_keywords').split(',')
    print 'Keywords parsed:', KEYWORDS
    print type(KEYWORDS)

    # Checking if keyword exists in KEYWORDS
    if keyword in KEYWORDS:
        print 'Keyword', keyword, 'exists in Configuration file'
    else:
        print 'Keyword', keyword, 'not found in Configuration file, adding.'
        appended_string = config.get('Keywords', 'twitter_keywords')
        appended_string = appended_string + ',' + keyword
        config.set('Keywords','twitter_keywords',appended_string)
        with open('./configurations.txt', 'w') as configfile: config.write(configfile)

# function that pulls tweets from twitter
def startTwitterRequests():
    print ('Fetching tweets started at ', str(time.ctime(time.time())))
    startStream()

# EB looks for an 'application' callable by default.
application = Flask(__name__)
socketio = SocketIO(application)

def fetchNewsArticles():
    startFetch()

# EB looks for an 'application' callable by default.
application = Flask(__name__)

@application.route('/gdelt')
def GDELT_root():
    # Loading initial values
    return render_template('MapTest.html')

@application.route('/')
def api_root():
    # Loading initial values
    return render_template('test.html')
    # return 'Welcome'

#Searches Tweets based on a Keyword
@application.route('/search/<keyword>')
def searchKeyword(keyword):
    configChanger(keyword)
    searchTweets = TwitterHandler()
    result = searchTweets.getTweets(keyword)
    return jsonify(result)

#Searches Tweets based on Keyword and Distance
@application.route('/search/<keyword>/<distance>/<latitude>/<longitude>')
def searchKeywordWithDistance(keyword, distance, latitude, longitude):
    searchTweets = TwitterHandler()
    result = searchTweets.getTweetsWithDistance(keyword, distance, latitude, longitude)
    return jsonify(result)

# Graph End point
@application.route('/graph/<keyword>/<start_time>/<end_time>/<latitude>/<longitude>')
def populate_graph(keyword, start_time, end_time, latitude, longitude):
    collated_emotions = graph_emotion_aggregates(keyword, latitude, longitude, start_time, end_time)
    context = dict(collated_emotions = collated_emotions)
    print ('Aggregated Emotions:', context)
    return jsonify(context)

#Searches Tweets, extracts max emotion and outputs news
@application.route('/news/<keyword>/<start_time>/<end_time>/<latitude>/<longitude>')
def sentiment_mapper(keyword, start_time, end_time, latitude, longitude):
    # Code to fetch tweets and find maximum emotion

    collated_emotions = graph_emotion_aggregates(keyword, latitude, longitude, start_time, end_time)

    joy_list = collated_emotions[0]
    anger_list = collated_emotions[1]
    sadness_list = collated_emotions[2]
    disgust_list = collated_emotions[3]
    fear_list = collated_emotions[4]

    value_joy = sum(joy_list.values())
    value_angry = sum(anger_list.values())
    value_fear = sum(sadness_list.values())
    value_disgust = sum(disgust_list.values())
    value_sadness = sum(fear_list.values())

    switcher = {
        value_angry:'anger',
        value_disgust:'disgust',
        value_fear:'fear',
        value_joy:'joy',
        value_sadness:'sadness'
        }

    max_emotion = switcher.get(max(value_angry, value_disgust, value_fear, value_joy, value_sadness),'default')
    print ('This is the max emotion', max_emotion)

    news_handler = NewsHandler()
    news_result = news_handler.getNewsWithDistance(latitude, longitude, start_time, end_time, max_emotion, keyword)
    print ('Output for news result')
    #print (news_result)
    print ('----------------------------------------')
    return jsonify(news_result)

#---- Flask SocketIO Implementation
@socketio.on('json')
def handle_json(json):
    print('Received json: ' + str(json))
    send(json, json=True)

# HTTP Endpoint for SNS
@application.route('/search/sns', methods=['GET', 'POST', 'PUT'])
def snsFunction():
    try:
        # Notification received from SNS
        print ('Notification received from SNS')
        print 'Request received', request
        if (len(request.data)):
            notification = json.loads(request.data)
        else:
            notification = request.form['hello']
    except:
        print("Unable to load request")
        pass

    headers = request.headers.get('X-Amz-Sns-Message-Type')


    print 'Headers is', headers
    print '**************************************'



    # print(notification)

    if headers == 'SubscriptionConfirmation' and 'SubscribeURL' in notification:
        url = requests.get(notification['SubscribeURL'])
        # print(url)
    elif headers == 'Notification':
        print ("I am here!!")
        TweetPersister.persistTweet(notification)
        #socketio.emit('first', {'notification': 'New Tweet!'})
    else:
        # print 'Value of headers', headers
        print("Headers not specified")
    return ('End point was accessed!')

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.

    twitter_thread = threading.Thread(target=startTwitterRequests)
    twitter_thread.daemon = True
    twitter_thread.start()
    thread.start_new_thread(fetchNewsArticles,())
    application.debug = True
    application.run()
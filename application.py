import json
import thread

#from TweetListener import *
from flask import Flask, render_template, jsonify

from TweetHandler import TwitterHandler
from  search_in_ES import FreeSearch
import threading
from flask_socketio import SocketIO, send, emit
from TweetListener import *
from flask import Flask, render_template, jsonify, request
from TweetHandler import TwitterHandler
import TweetPersister
import time
from news import NewsHandler as ne
import requests


#----------------------------------------
# News Fetching and Handling API
from news import NewsHandler
from news.NewsListener import *
#----------------------------------------


# function that pulls tweets from twitter
def startTwitterRequests():
    print 'Fetching tweets started at ', str(time.ctime(time.time()))
    startStream()

# EB looks for an 'application' callable by default.
application = Flask(__name__)
socketio = SocketIO(application)

def fetchNewsArticles():
    startFetch()

# EB looks for an 'application' callable by default.
application = Flask(__name__)

@application.route('/')
def api_root():
    return render_template('index.html')
    # return 'Welcome'

'''
Searches Tweets based on a Keyword
@application.route('/search/<keyword>')
def searchKeyword(keyword):
    searchTweets = TwitterHandler()
    result = searchTweets.getTweets(keyword)
    return jsonify(result)'''

'''
Searches Tweets based on Keyword and Distance
@application.route('/search/<keyword>/<distance>/<latitude>/<longitude>')
def searchKeywordWithDistance(keyword, distance, latitude, longitude):
    searchTweets = TwitterHandler()
    result = searchTweets.getTweetsWithDistance(keyword, distance, latitude, longitude)
    return jsonify(result)
'''

@application.route('/search/')
def sentiment_mapper():
    
    # Below variable function NEEDS TO BE CHECKED !!!!!!!!!!!!!!!
    t_start = request.args.get('time_start')
    t_end = request.args.get('time_end')
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')

    # Code to fetch tweets and find maximum emotion

    # NACHIKET: INSERT CODE HERE

    # By this point variable max_emotion should be available
    max_emotion="anger"
    # Code to fetch news from ES based on max_emotion

    # AKHILESH AND AKANKSHA: insert code here- we have time-tstart, tend, location-latitude and longitude and max emotion.
    news_result=ne.NewsHandler.getNewsWithDistance(latitude, longitude, t_start, t_end, max_emotion)
    return jsonify(news_result)

# Route of ES search for free keyword search
@application.route('/freesearch/<keyword>')
def freesearchKeyword(keyword):
    searchTweets = FreeSearch()
    result = searchTweets.getKeywordSearchTweets(keyword)
    return jsonify(result)

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
        print 'Notification received from SNS'
        if (len(request.data)):
            notification = json.loads(request.data)
        else:
            notification = request.form['hello']
    except:
        print("Unable to load request")
        pass

    headers = request.headers.get('X-Amz-Sns-Message-Type')
    # print(notification)

    if headers == 'SubscriptionConfirmation' and 'SubscribeURL' in notification:
        url = requests.get(notification['SubscribeURL'])
        # print(url)
    elif headers == 'Notification':
        print "I am here!!"
        TweetPersister.persistTweet(notification)
        socketio.emit('first', {'notification': 'New Tweet!'})
    else:
        # print 'Value of headers', headers
        print("Headers not specified")
    return 'End point was accessed!'


# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    #thread.start_new_thread(startTwitterRequests, ())
    print 'Running application.py'
    # thread.start_new_thread(fetchNewsArticles,())
    #application.debug = True
    twitter_thread = threading.Thread(target=startTwitterRequests)
    twitter_thread.daemon = True
    twitter_thread.start()
    application.run()
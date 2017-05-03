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
import requests


#----------------------------------------
# News Fetching and Handling API
from news import NewsHandler
from news.NewsListener import *
#----------------------------------------


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

    # Code to fetch news from ES based on max_emotion

    # AKHILESH AND AKANKSHA: insert code here

    def getKeywordSearchTweets(start_time, end_time, latitude, longitude):
        value_joy = 0
        value_angry = 0
        value_fear = 0
        value_disgust = 0
        value_sadness = 0
        EMOVALUE=[]
        starttime = request.args.get('start_time')
        endtime = request.args.get('end_time')
        lat = request.args.get('latitude')
        lon = request.args.get('longitude')
        es = ElasticSearchServices()
        index = "newsdomain3"
        doc_type = "finaltweets2"
        body = {
        "query":{
                    "bool" : {
                        "must" : [
                            {"match":{"sentiment":"neutral"}}
                            ],
                        "must_not":
                            {"range": {
                        "timestamp":{
                            "gte": "now",
                            "lte": "2016"
                        }
                     }
                    },
                "filter":{
                "geo_distance" : {
                    "distance" : "2000km",
                    "location" : {
                        "lat" : 40.06889420539272,
                        "lon" : -120.32554198435977
                    }
                }
            }

            }
        }
        }

        size = 10000
        result = es.search(index, doc_type, body, size)

        value_angry = value_angry + result['angry']
        EMOVALUE.append(value_angry)
        value_disgust = value_disgust + result['disgust']
        EMOVALUE.append(value_disgust)
        value_fear = value_fear + result['fear']
        EMOVALUE.append(value_fear)
        value_joy = value_joy + result['joy']
        EMOVALUE.append(value_joy)
        value_sadness = value_sadness + result['sadness']
        EMOVALUE.append(value_sadness)




        return EMOVALUE



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
        print ('Notification received from SNS')
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
        # print 'Persisting in Elastic BeanStalk'
        # print 'Normal Notification'
        # print'---------------------'
        # print notification
        # print 'Type is :', type(notification)
        # print '-------------------------'
        # print 'Json.loads result of notification'
        # print '---------------------------------'
        # print (notification['Message'])
        # print 'Type is :', type((notification['Message']))
        # print '-------------------------'
        print ("I am here!!")
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
    print ('Running application.py')
    # thread.start_new_thread(fetchNewsArticles,())
    application.debug = True
    twitter_thread = threading.Thread(target=startTwitterRequests)
    twitter_thread.daemon = True
    twitter_thread.start()
    application.run()

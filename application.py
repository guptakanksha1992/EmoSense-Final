import json
import thread

from TweetListener import *
from flask import Flask, render_template, jsonify

from TweetHandler import TwitterHandler

#----------------------------------------
# News Fetching and Handling API
from news import NewsHandler
from news.NewsListener import *
#----------------------------------------

# Graph Populating code
from GraphHandler import *
#----------------------------------------


# function that pulls tweets from twitter
def startTwitterRequests():
    print "Starting the wrong function"
    startStream()


def fetchNewsArticles():
    startFetch()

# EB looks for an 'application' callable by default.
application = Flask(__name__)

@application.route('/')
def api_root():
    # Loading initial values
    return render_template('test.html')
    # return 'Welcome'

@application.route('/search/<keyword>')
def searchKeyword(keyword):
    searchTweets = TwitterHandler()
    result = searchTweets.getTweets(keyword)
    return jsonify(result)

@application.route('/search/<keyword>/<distance>/<latitude>/<longitude>')
def searchKeywordWithDistance(keyword, distance, latitude, longitude):
    searchTweets = TwitterHandler()
    result = searchTweets.getTweetsWithDistance(keyword, distance, latitude, longitude)
    return jsonify(result)

# Graph End point
@application.route('/graph/<start_time>/<end_time>/<latitude>/<longitude>')
def populate_graph(start_time, end_time, latitude, longitude):
    collated_emotions = graph_emotion_aggregates(start_time, end_time, latitude, longitude)
    context = dict(collated_emotions = collated_emotions)
    print 'Aggregated Emotions:', context
    return jsonify(context)

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    thread.start_new_thread(startTwitterRequests, ())
    #thread.start_new_thread(fetchNewsArticles,())
    application.debug = True
    application.run()
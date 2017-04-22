# Importing Natural Language Processing libraries

import sys
from watson_developer_cloud import NaturalLanguageUnderstandingV1
import watson_developer_cloud.natural_language_understanding.features.v1 as features
import re
import ConfigParser

# --------------------------------------------------------------------------------------------------

reload(sys)
sys.setdefaultencoding('utf8')
config = ConfigParser.ConfigParser()
config.readfp(open(r'./configurations.txt'))

HOST = config.get('ES Instance', 'elastic_search_host_address')
PORT = config.get('ES Instance', 'Port')


Username = config.get('Watson Credentials', 'Username')
Password = config.get('Watson Credentials', 'Password')

natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2017-02-27',
    username=Username,
    password=Password)


def sentimentAnalysis(text):
    try:
        # Remove unwanted special characters from text
        correct_text = re.sub('[^a-zA-Z0-9 \n\.]', '', text)
        # encoded_text = urllib.quote(text)
        response = natural_language_understanding.analyze(
            text=correct_text,
            features=[features.Emotion(), features.Sentiment()])

        emotion_dict = response['emotion']['document']['emotion']
        overall_sentiment = response['sentiment']['document']['label']

        return overall_sentiment, emotion_dict

    except Exception, e:
        print 'Sentiment API error ' + str(e)


def clean_tweet(tweet):
    '''
    Utility function to clean tweet text by removing links, special characters
    using simple regex statements.
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())


def tweet_sentiment_analysis(tweet):
    cleansed_tweet = clean_tweet(tweet)
    # Sentiment analysis on title
    sentiment, allemotions = sentimentAnalysis(cleansed_tweet)
    anger = allemotions['anger']
    joy = allemotions['joy']
    sadness = allemotions['sadness']
    fear = allemotions['fear']
    disgust = allemotions['disgust']

    return sentiment,anger,joy,sadness,fear,disgust

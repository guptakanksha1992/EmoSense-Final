import  json
import re
import ConfigParser
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from watson_developer_cloud import NaturalLanguageUnderstandingV1
import watson_developer_cloud.natural_language_understanding.features.v1 as \
    features

config = ConfigParser.ConfigParser()
config.readfp(open(r'./configurations.txt'))

HOST = config.get('ES Instance', 'Host')
PORT = config.get('ES Instance', 'Port')

#consumer key, consumer secret, access token, access secret.
ckey = config.get('Twitter API Keys', 'ConsumerKey')
csecret = config.get('Twitter API Keys', 'ConsumerSecret')
atoken = config.get('Twitter API Keys', 'AccessToken')
asecret = config.get('Twitter API Keys', 'AccessSecret')

index = "emoSenseindex"

#watson username and password
wusername = config.get('Watson Credentials','Username')
wpassword = config.get('Watson Credentials','Password')

natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2017-02-27',
    username=wusername,
    password=wpassword)

def sentimentAnalysis(text):
    #encoded_text = urllib.quote(text)
    response = natural_language_understanding.analyze(
        text=text,
        features=[features.Emotion(),features.Sentiment()])
    #print text
    emotion_dict = response['emotion']['document']['emotion']
    overall_sentiment = response['sentiment']['document']['label']

    #print ("The overall sentiment of the text is: "+overall_sentiment)
    print ("The emotional quotient of the text is as follows: ")
    for key in emotion_dict:
        print (key+" : "+str(emotion_dict[key]))
    return overall_sentiment

def clean_tweet(tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

class listener(StreamListener):

    def on_data(self, data):
        #tweet = data.split(',"text":"')[1].split('","source')[0]
        tweet = clean_tweet(json.loads(data)["text"])
        #print tweet
        sentimentRating = sentimentAnalysis(tweet)
        saveMe = tweet+'::'+sentimentRating+'\n'
        output = open('output.csv','a')
        output.write(saveMe)
        output.close()
        return(True)

    def on_error(self, status):
        print status

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener())
twitterStream.filter(languages=["en"],track=["car"])

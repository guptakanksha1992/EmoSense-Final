import json
from NewsHandler import NewsHandler
from ElasticSearchServices import ElasticSearchServices
import random,operator
import ConfigParser
import requests

f = open("API_KEY.txt")
api_key = f.read()
config = ConfigParser.ConfigParser()
config.readfp(open(r'./configurations.txt'))
#----------------------------------
# Sentiment Analysis
import re
import sys
from watson_developer_cloud import NaturalLanguageUnderstandingV1
import watson_developer_cloud.natural_language_understanding.features.v1 as features
#----------------------------------

KEYWORDS = ['Sports', 'Politics', 'Technology', 'Health', 'Entertainment']
REQUEST_LIMIT = 420

index = "news2"
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
				},
                "sentiment": {
                    "type": "string"
                },
                "dominant_emotion": {
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

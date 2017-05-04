import ConfigParser
from elasticsearch import Elasticsearch
from datetime import datetime
import certifi
import ast,json
from flask import Flask, render_template, jsonify, request

config = ConfigParser.ConfigParser()
config.readfp(open(r'./configurations.txt'))

HOST = config.get('ES Instance', 'elastic_search_host_address')
PORT = config.get('ES Instance', 'Port')

size = 100

def graph_emotion_aggregates(keyword, latitude, longitude, start_time, end_time):

    if (type(latitude) != float):
        latitude = float(latitude)

    if (type(longitude) != float):
        longitude = float(longitude)

    es = Elasticsearch(
            HOST,
            port=int(PORT),
            use_ssl = 'True'
        )

    body = {
        "query":{
                    "bool" : {
                        "must": [
                            {"range": {
                        "timestamp":{
                            "lte": end_time,
                            "gte": start_time
                        }
                     }}
                    ],
                "filter":{
                "geo_distance" : {
                    "distance" : "1000km",
                    "location" : {
                        "lat" : latitude,
                        "lon" : longitude
                    }
                }
            }

            }
        }
    }

    results = es.search(
            index = 'newsdomain3',
            doc_type = 'finaltweets2',
            body = body,
            size = size
        )


    joy_dict = {}
    anger_dict = {}
    sadness_dict = {}
    disgust_dict = {}
    fear_dict = {}
    dict_array = []
    joy_val = 0.0
    anger_val = 0.0
    sadness_val = 0.0
    disgust_val = 0.0
    fear_val = 0.0

    for result in results['hits']['hits']:
        #print result['_source']
        timestamp_strings = result['_source']['timestamp'].split()
        timestamp_hash =  timestamp_strings[-1]+timestamp_strings[1]+timestamp_strings[2]

        joy_val =  result['_source']['joy']
        if timestamp_hash in joy_dict:
            joy_val = joy_val + joy_dict[timestamp_hash]

        anger_val =  result['_source']['anger']
        if timestamp_hash in anger_dict:
            anger_val = anger_val + anger_dict[timestamp_hash]

        sadness_val =  result['_source']['sadness']
        if timestamp_hash in sadness_dict:
            sadness_val = sadness_val + sadness_dict[timestamp_hash]

        disgust_val =  result['_source']['disgust']
        if timestamp_hash in disgust_dict:
            disgust_val = disgust_val + disgust_dict[timestamp_hash]

        fear_val =  result['_source']['fear']
        if timestamp_hash in fear_dict:
            fear_val = fear_val + fear_dict[timestamp_hash]


        joy_dict[timestamp_hash] = joy_val
        anger_dict[timestamp_hash] = anger_val
        sadness_dict[timestamp_hash] = sadness_val
        disgust_dict[timestamp_hash] = disgust_val
        fear_dict[timestamp_hash] = fear_val


    dict_array.append(joy_dict)
    dict_array.append(anger_dict)
    dict_array.append(sadness_dict)
    dict_array.append(disgust_dict)
    dict_array.append(fear_dict)

    #print dict_array
    return dict_array
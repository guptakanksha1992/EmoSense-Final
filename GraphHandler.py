from ElasticSearchServices import ElasticSearchServices

size = 100

def graph_emotion_aggregates(start_time, end_time, latitude, longitude):

    if (type(latitude) != float):
            latitude = float(latitude)

    if (type(longitude) != float):
        longitude = float(longitude)

    #print 'Start time:', start_time, 'End time:', end_time, 'Latitude:', latitude, 'Longitude:', longitude

    # Elastic Search service object
    es = ElasticSearchServices()

    body = {
        "query":{
                    "bool" : {
                        "must": [
                            {"range": {
                        "timestamp":{
                            "lte": start_time,
                            "gte": end_time
                        }
                     }}
                    ],
                "filter":{
                "geo_distance" : {
                    "distance" : "5000km",
                    "location" : {
                        "lat" : latitude,
                        "lon" : longitude
                    }
                }
            }

            }
        }
    }

    size = 10000
    results = es.search(
            index = 'newsdomain3',
            doc_type = 'finaltweets2',
            body = body,
            size = size
        )



    daily_collated_emotions_dict = {}

    for result in results['hits']['hits']:
        timestamp_strings = result['_source']['timestamp'].split()
        timestamp_hash =  timestamp_strings[-1]+timestamp_strings[1]+timestamp_strings[2]
        emotions_array =  [0.0, 0.0, 0.0, 0.0, 0.0]
        if timestamp_hash in daily_collated_emotions_dict:
           emotions_array = daily_collated_emotions_dict[timestamp_hash]
        daily_collated_emotions_dict[timestamp_hash] = \
                                                    [emotions_array[0]+result['_source']['joy'],
                                                     emotions_array[1]+result['_source']['anger'],
                                                     emotions_array[2]+result['_source']['sadness'],
                                                     emotions_array[3]+result['_source']['disgust'],
                                                     emotions_array[4]+result['_source']['fear']
                                                     ]

    return daily_collated_emotions_dict

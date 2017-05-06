from ElasticSearchServices import ElasticSearchServices


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

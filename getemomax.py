from ElasticSearchServices import ElasticSearchServices


def getKeywordSearchTweets(keyword, latitude, longitude, starttime, endtime):
    starttime = request.args.get('starttime')
    endtime = request.args.get('endtime')
    location = request.args.get('location')
    es = ElasticSearchServices()
    index = "newsdomain3"
    doc_type = "finaltweets2"
    body = {
    "query":{
                "bool" : {
                    "must" : [
                        {"match":{"dominant_emotion":"sadness"}},
                        {"range": {
                    "timestamp":{
                        "gte": "2017-04-23",
                        "lte": "now"
                    }
                 }
                }
                        ],
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

    return result

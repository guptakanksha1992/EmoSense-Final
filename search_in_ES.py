from ElasticSearchServices import ElasticSearchServices

class FreeSearch:

    def getKeywordSearchTweets(keyword):
        es = ElasticSearchServices()
        index = "emosense_index"
        doc_type = "finaltweets2"
        body = {
            "query": {
                "match": {
                    "_all": keyword
                }
            }
        }

        size = 10000
        result = es.search(index, doc_type, body, size)
        return result
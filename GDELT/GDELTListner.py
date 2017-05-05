import ConfigParser
from bigquery.client import get_client

def fetchGDELT(timestamp, latitude, longitude):

    #  BigQuery project id as listed in the Google Developers Console.
    project_id = 'mycloudproject-165020'

    # Service account email address as listed in the Google Developers Console.
    service_account = 'gunnernet@mycloudproject-165020.iam.gserviceaccount.com'

    # PKCS12 or PEM key provided by Google.
    key = 'mykey.json'
    client = get_client(json_key_file=key, readonly=True)
    #"1979-01-23T06:59:58Z" 18.23733106276245,
    #79.54300905036112

    event = {"timestamp": timestamp,
             "location": [latitude ,  longitude]
    }
    # def lambda_handler(event, context):
    M = []

    a = (event['timestamp'])
    a = (a[0:10])
    date1 = a.replace('-', '')
    print (date1)
    try:
        # Submit an async query.
        # job_id, _results = client.query("""SELECT * FROM dataset.my_table LIMIT 1000""")

        # Check if the query has finished running.

        job_id, _results  = client.query("""SELECT GLOBALEVENTID,GoldsteinScale,SOURCEURL FROM [gdelt-bq:full.events] WHERE (SQLDATE BETWEEN {0} AND {1}) AND (ACOS( SIN( RADIANS( ActionGeo_Lat ) ) * SIN( RADIANS( {2}) ) + COS( RADIANS( ActionGeo_Lat ) )
        * COS( RADIANS( {2} )) * COS( RADIANS( ActionGeo_Long ) - RADIANS( {3} )) ) * 6371 <= 1000)
        ORDER BY GoldsteinScale DESC LIMIT 20""".format(date1, date1-10, latitude,  longitude))

        results = client.get_query_rows(job_id)
        # return (results)
        for r in results:
            M.append(r['SOURCEURL'])
        print M

    except Exception as e:
        print (str(e))

def startGDELTFetch(timestamp, latitude, longitude):
        try:
            print 'Fetching GDELT Data!'
            fetchGDELT(timestamp, latitude, longitude)
        except Exception, e:
            print("Exception in fetching GDELT Data:" + str(e))

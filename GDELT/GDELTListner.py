from bigquery.client import get_client

def fetchGDELT(timestamp, latitude, longitude):
    # BigQuery project id as listed in the Google Developers Console.
    project_id = 'mycloudproject-165020'

    # Service account email address as listed in the Google Developers Console.
    service_account = 'gunnernet@mycloudproject-165020.iam.gserviceaccount.com'

    # PKCS12 or PEM key provided by Google.
    key = 'mykey.json'

    client = get_client(json_key_file=key, readonly=True)

    event = {"timestamp": timestamp,
    "location": [
                      latitude,
                      longitude
                   ]
    }
    print (timestamp)
    print (event)

    M=[]
    lat =  (event['location'][0])
    longitude = (event['location'][1])

    a = (event['timestamp'])
    a = (a[0:10])
    date = a.replace('-','')
    print (date)
    try:
        job_id, _results  = client.query("""SELECT GLOBALEVENTID,GoldsteinScale,SOURCEURL FROM [gdelt-bq:full.events] WHERE (SQLDATE BETWEEN {0} AND {1}) AND (ACOS( SIN( RADIANS( ActionGeo_Lat ) ) * SIN( RADIANS( {2} ) ) + COS( RADIANS( ActionGeo_Lat ) )
        * COS( RADIANS( {2} )) * COS( RADIANS( ActionGeo_Long ) - RADIANS( {3} )) ) * 6371 <= 1000)
        ORDER BY GoldsteinScale DESC LIMIT 20""".format("19790119",date,latitude,longitude))

        complete, row_count = client.check_job(job_id)
        results = client.get_query_rows(job_id)
        # return (results)
        for r in results:
             M.append(r['SOURCEURL'])
        print (M)
    except Exception as e:
        print (str(e))




# def startGDELTFetch():
#     try:
#         print 'Fetching GDELT Data!'
#         fetchGDELT("1979-01-23T06:59:58Z", 18.23733106276245, 79.54300905036112)
#     except Exception, e:
#         print("Exception in fetching GDELT Data:" + str(e))

try:
    print 'Fetching GDELT Data!'
    fetchGDELT("1979-01-23T06:59:58Z", 18.23733106276245, 79.54300905036112)
except Exception, e:
    print("Exception in fetching GDELT Data:" + str(e))

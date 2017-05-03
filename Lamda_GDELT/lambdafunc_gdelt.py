from bigquery.client import get_client
from bigquery.query_builder import render_query
from geopy.geocoders import Nominatim

# BigQuery project id as listed in the Google Developers Console.
project_id = 'mycloudproject-165020'

# Service account email address as listed in the Google Developers Console.
service_account = 'gunnernet@mycloudproject-165020.iam.gserviceaccount.com'

# PKCS12 or PEM key provided by Google.
key = 'mykey.json'

#client = get_client(project_id, service_account=service_account,
#                    private_key_file=key, readonly=True)

client = get_client(json_key_file=key, readonly=True)
geolocator = Nominatim()

#def lambda_handler(event, context):
event = {"timestamp": "2017-04-22T06:59:58Z",
"location": [
                  52.509669,
                  13.376294
               ]
}
lat =  (event['location'][0])
longitude = (event['location'][1])
print (lat)
print (longitude)
location = geolocator.reverse((str(lat), str(longitude)))
print (location.raw)
# location.raw['address']['country'].upper()
#
a = (event['timestamp'])
a = (a[0:10])
date = a.replace('-','')
print (date)
try:
    selects = {
        'SQLDATE': {
            'alias': 'SQLDATE',
            'format': 'INTEGER-FORMAT_UTC_USEC'
        }
    }

    conditions = [
        {
            'field': 'SQLDATE',
            'type': 'INTEGER',
            'comparators': [
                {
                    'condition': '==',
                    'negate': False,
                    'value': 19790123
                }
            ]
        }
    ]

    grouping = ['SQLDATE']

    having = [
        {
            'field': 'SQLDATE',
            'type': 'INTEGER',
            'comparators': [
                {
                    'condition': '==',
                    'negate': False,
                    'value': 19790123
                }
            ]
        }
    ]

    order_by ={'fields': ['SQLDATE'], 'direction': 'desc'}

    query = render_query(
        'gdelt-bq:full',
        ['events'],
        select=selects,
        conditions=conditions,
        groupings=grouping,
        having=having,
        order_by=order_by,
        limit=47
    )
    job_id, _results = client.query('''SELECT * FROM [gdelt-bq:full.events] WHERE (SQLDATE BETWEEN 19790123 AND 19790323) AND (ActionGeo_Lat BETWEEN 32.8191 AND 34.8191)
    AND (ActionGeo_Long BETWEEN -81.9066 AND -79.9066)
    ORDER BY GoldsteinScale DESC LIMIT 200 ''')

    #job_id, _results = client.query(query)
    # job_id, _results  = client.query("""SELECT SQLDATE SQLDATE, INTEGER(norm*100000)/1000 Percent FROM (
    # SELECT EventRootCode, SQLDATE, GoldsteinScale, COUNT(1) AS c, RATIO_TO_REPORT(c) OVER(PARTITION BY SQLDATE ORDER BY c DESC) norm FROM [gdelt-bq:full.events]
    # GROUP BY EventRootCode, SQLDATE, GoldsteinScale)
    # WHERE SQLDATE = 19790123
    # ORDER BY GoldsteinScale""".format(date))

    complete, row_count = client.check_job(job_id)
    results = client.get_query_rows(job_id)
    #print (results)
    for r in results:
          print (r['GoldsteinScale'])
except Exception as e:
    print (str(e))
#     print ("This gives you an error")

from bigquery.client import get_client
from bigquery.query_builder import render_query

# BigQuery project id as listed in the Google Developers Console.
project_id = 'mycloudproject-165020'

# Service account email address as listed in the Google Developers Console.
service_account = 'gunnernet@mycloudproject-165020.iam.gserviceaccount.com'

# PKCS12 or PEM key provided by Google.
key = 'mykey.pem'

client = get_client(project_id, service_account=service_account,
                    private_key_file=key, readonly=True)


selects = {
    'start_time': {
        'alias': 'Timestamp',
        'format': 'INTEGER-FORMAT_UTC_USEC'
    }
}

conditions = [
    {
        'field': 'GoldsteinScale',
        'type': 'FLOAT',
        'comparators': [
            {
                'condition': '>=',
                'negate': False,
                'value': 3.0
            }
        ]
    }
]

grouping = ['Timestamp']

having = [
    {
        'field': 'Timestamp',
        'type': 'INTEGER',
        'comparators': [
            {
                'condition': '==',
                'negate': False,
                'value': 1399478981
            }
        ]
    }
]

order_by ={'fields': ['Timestamp'], 'direction': 'desc'}

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








try:

     #job_id, _results = client.query('SELECT * FROM [gdelt-bq:full.events] WHERE GoldsteinScale = 3.0 LIMIT 10')
     #job_id, _results = client.query('SELECT * FROM [gdelt-bq:extra.toytonelookup]  LIMIT 1000')
     #job_id, _results = client.query('SELECT * FROM [gdelt-bq:internetarchivebooks]  LIMIT 1000')
     job_id, _results = client.query(query)
     complete, row_count = client.check_job(job_id)
     results = client.get_query_rows(job_id)
     #print (results["GoldsteinScale"])
     print (results)
except Exception as e:
    print (str(e))
    #print ("This gives you an error")

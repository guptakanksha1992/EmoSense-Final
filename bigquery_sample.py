from bigquery.client import get_client

# BigQuery project id as listed in the Google Developers Console.
project_id = 'mycloudproject-165020'

# Service account email address as listed in the Google Developers Console.
service_account = 'gunnernet@mycloudproject-165020.iam.gserviceaccount.com'

# PKCS12 or PEM key provided by Google.
key = 'mykey.pem'

client = get_client(project_id, service_account=service_account,
                    private_key_file=key, readonly=True)





# JSON key provided by Google
# json_key = 'newkey.json'
#
# client = get_client(json_key_file=json_key, readonly=True)

# Submit an async query.

try:
     job_id, _results = client.query('SELECT * FROM [gdelt-bq:full.events] LIMIT 1000')
     complete, row_count = client.check_job(job_id)
     results = client.get_query_rows(job_id)
     print (results)
except:
    print ("This gives you an error")


# job_id, _results = client.query('SELECT MonthYear MonthYear, INTEGER(norm*100000)/1000 Percent
# FROM (
# SELECT ActionGeo_CountryCode, EventRootCode, MonthYear, COUNT(1) AS c, RATIO_TO_REPORT(c) OVER(PARTITION BY MonthYear ORDER BY c DESC) norm FROM [gdelt-bq:full.events]
# GROUP BY ActionGeo_CountryCode, EventRootCode, MonthYear
# )
# WHERE ActionGeo_CountryCode='UP' and EventRootCode='14'
# ORDER BY ActionGeo_CountryCode, EventRootCode, MonthYear;


#

#
# # Retrieve the results.
results = client.get_query_rows(job_id)

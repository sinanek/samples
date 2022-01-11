import sys
import os
import requests
import google.auth
import google.auth.transport.requests
import json
import time
from  datetime import datetime, timezone
from google.cloud import storage,bigquery
from six import iteritems
creds, project = google.auth.default()

# creds.valid is False, and creds.token is None
# Need to refresh credentials to populate those

auth_req = google.auth.transport.requests.Request()
creds.refresh(auth_req)





current_time = time.time()
print(current_time)
prev_time = 1639554700


#{}
#[]
BUCKET_NAME = "sina-emea-sce01-us"
CDF_INSTANCE_ID="cdf_instance"
CDF_REGION="us-west1"
CDF_PIPELINE="bq-arg-setter_v2"
NAMESPACE="default"
REGION="US"
CDF_ENDPOINT="https://dev-cdf-donuts-sina-emea-sce01-dot-euw4.datafusion.googleusercontent.com/api/v3/"
header = {"Authorization": "Bearer "+creds.token}
#namespaces/default/apps/bq-arg-setter_v2/workflows/DataPipelineWorkflow/runs"
def get_run_details(pipeline_name):
    url = f"{CDF_ENDPOINT}namespaces/{NAMESPACE}/apps/{pipeline_name}/workflows/DataPipelineWorkflow/runs"
    response = requests.get(url,headers=header)
    if response:
        return response.json()

def parse_ts(timestamp,format = "%Y-%m-%d %H:%M:%S"):
    return datetime.fromtimestamp(timestamp).strftime(format)
    
def parse_run_details(runs,timestamp):
    parsed = []
    for run in runs:
        #only get finished runs
        if run['end'] > timestamp:
       
            run_parsed = {}
            run_parsed['pipeline_name'] = CDF_PIPELINE
            #convert to timestamp
            run_parsed['start_requested_dttm'] = parse_ts(run['starting'])
            run_parsed['start_dttm'] = parse_ts(run['start'])
            run_parsed['end_dttm'] = parse_ts(run['end'])
            #create new duration metric
            run_parsed['job_duration_mins'] = round((run['end'] - run['start'])/60,2)
            run_parsed['total_duration_mins'] = round((run['end'] - run['starting'])/60,2)
            
            run_parsed['status'] = run['status']
            run_parsed['properties'] = str({k:v for k,v in json.loads(run['properties']['runtimeArgs']).items() if k != "logical.start.time" })
            run_parsed['create_dttm'] = parse_ts(current_time)
            
    return  run_parsed

def upload_file(destination_blob_name,obj):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(BUCKET_NAME)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(obj)

    print('Object uploaded to {}.'.format(
        destination_blob_name))

def write_to_bq(table_id,source):
    bq_client = bigquery.Client()

    # TODO(developer): Set table_id to the ID of the table to create.
    # table_id = "your-project.your_dataset.your_table_name"

    job_config = bigquery.LoadJobConfig(
    create_disposition = bigquery.CreateDisposition.CREATE_IF_NEEDED,
    source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
    write_disposition = bigquery.WriteDisposition.WRITE_APPEND
    )
    uri = f"gs://{BUCKET_NAME}/{source}"

    load_job = bq_client.load_table_from_uri(
    uri,
    table_id,
    location=REGION,  # Must match the destination dataset location.
    job_config=job_config,
    )  # Make an API request.

    load_job.result()  # Waits for the job to complete.

    destination_table = bq_client.get_table(table_id)
    print("Loaded {} rows.".format(destination_table.num_rows))

obj = parse_run_details(get_run_details(CDF_PIPELINE),prev_time)
#print(obj)
print(json.dumps(obj))
upload_file("run.json",json.dumps(obj))
write_to_bq('sina-emea-sce01.datafusion.runs','run.json')
#last_run_id=`curl -s -X GET -H "Authorization: Bearer ${AUTH_TOKEN}" "${CDAP_ENDPOINT}/v3/namespaces/default/apps/${CDF_PIPELINE}/workflows/DataPipelineWorkflow/runs" | jq -r '.[0].runid'`

#[{'runid': 'd90e7783-5d7a-11ec-8d71-62299fe599ea', 'starting': 1639554275, 'start': 1639554466, 'end': 1639554739, 'status': 'COMPLETED', 'properties': {'runtimeArgs': '{"logical.start.time":"1639554275064","system.profile.name":"SYSTEM:dataproc","datasetprojectid":"sina-emea-sce02"}', 'phase-2': '5810f671-5d7b-11ec-9097-42010aa40013'}, 'cluster': {'status': 'DEPROVISIONED', 'end': 1639554777, 'numNodes': 1}, 'profile': {'profileName': 'dataproc', 'namespace': 'system', 'entity': 'PROFILE'}}, {'runid': 'c3eb4dde-2060-11ec-a36b-4e335a7e8d3a', 'starting': 1632836051, 'start': 1632836219, 'end': 1632836501, 'status': 'COMPLETED', 'properties': {'runtimeArgs': '{"logical.start.time":"1632836051757","system.profile.name":"SYSTEM:dataproc"}', 'phase-2': '35626481-2061-11ec-bef1-42010aa4002c'}, 'cluster': {'status': 'DEPROVISIONED', 'end': 1632836537, 'numNodes': 1}, 'profile': {'profileName': 'dataproc', 'namespace': 'system', 'entity': 'PROFILE'}}]
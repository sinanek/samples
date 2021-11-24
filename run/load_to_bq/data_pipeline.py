# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START cloudrun_imageproc_handler_setup]
# [START run_imageproc_handler_setup]
import os

from google.cloud import storage, bigquery

storage_client = storage.Client()

def load_file(current_blob):
    file_name = current_blob["name"]
    client = bigquery.Client()
    staging_bucket_name = os.getenv("STAGING_BUCKET_NAME")
    processed_bucket_name = os.getenv("PROCESSED_BUCKET_NAME")
    table_id = os.getenv("TABLE_ID")

    job_config = bigquery.LoadJobConfig(source_format=bigquery.SourceFormat.AVRO,
    write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE)
    uri = f"gs://{staging_bucket_name}/{file_name}"

    load_job = client.load_table_from_uri(
        uri, table_id, job_config=job_config
    )  # Make an API request.

    load_job.result()  # Waits for the job to complete.

    destination_table = client.get_table(table_id)
    print("Loaded {} rows.".format(destination_table.num_rows))

    #move file to processed bucket
    source_bucket = storage_client.bucket(staging_bucket_name)

    source_blob = source_bucket.blob(file_name)
 
    destination_bucket = storage_client.bucket(processed_bucket_name)
 

    blob_copy = source_bucket.copy_blob(
        source_blob, destination_bucket, file_name
    )

    source_bucket.delete_blob(file_name)

    print(f"Blob {source_blob.name} in bucket {source_bucket.name} moved to blob {blob_copy.name} in bucket {destination_bucket.name}.")


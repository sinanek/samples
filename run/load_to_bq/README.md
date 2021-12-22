# Cloud Run Sample

This sample service applies [Cloud Storage](https://cloud.google.com/storage/docs)-triggered loading to bigquery

[![Run in Google Cloud][run_img]][run_link]


## Build

```
docker build --tag load-to-bq:python .
```

## Run Locally

```
docker run --rm -p 9090:8080 -e PORT=8080 load-to-bq:python
```

## Test

```
pytest
```

_Note: you may need to install `pytest` using `pip install pytest`._

## Deploy

```
# Set an environment variable with your GCP Project ID
export GOOGLE_CLOUD_PROJECT=<PROJECT_ID>

# Submit a build using Google Cloud Build
gcloud builds submit --tag gcr.io/${GOOGLE_CLOUD_PROJECT}/load-to-bq

# Deploy to Cloud Run
gcloud run deploy <APPLICATION_NAME> --image gcr.io/${GOOGLE_CLOUD_PROJECT}/load-to-bq --set-env-vars=STAGING_BUCKET_NAME=<STAGING_BUCKET_NAME>,PROCESSED_BUCKET_NAME=<PROCESSED_BUCKET_NAME>,TABLE_ID=<PROJECT_ID>.<DATASET_NAME>.<TABLE_NAME>

```

## Environment Variables

Cloud Run services can be [configured with Environment Variables](https://cloud.google.com/run/docs/configuring/environment-variables).
Required variables for this sample include:

* `STAGING_BUCKET_NAME`: The Cloud Run service will be notified of files uploaded to this Cloud Storage bucket. The service will then retrieve and process the file.
* `PROCESSED_BUCKET_NAME`: The Cloud Run service will move processed files to this Cloud Storage bucket.
* `TABLE_ID`: The table into which data is loaded.


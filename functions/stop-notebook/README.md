# Deploy function
```
gcloud beta functions deploy stop-idle-notebook \
--gen2 \
--region us-central1 \
--runtime python39 \
--trigger-http \
--entry-point stop_notebook \
--source . \
--allow-unauthenticated

```

Use the `--allow-unauthenticated` flag if needed
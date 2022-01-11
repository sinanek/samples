
create table datafusion.runs (
pipeline_name STRING,
start_requested_dttm TIMESTAMP,
start_dttm TIMESTAMP,
end_dttm TIMESTAMP,
job_duration_mins NUMERIC,
total_duration_mins NUMERIC,
status STRING,
properties STRING,
create_dttm TIMESTAMP)
PARTITION BY
  DATE_TRUNC(start_dttm, MONTH)
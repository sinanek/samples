import functions_framework
from google.cloud import notebooks_v1beta1 as np
import base64
import json

@functions_framework.http
def stop_notebook(request):
    """HTTP Cloud Function.
   Args:
       request (flask.Request): The request object.
       <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
   Returns:
       The response text, or any set of values that can be turned into a
       Response object using `make_response`
       <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
   """
    request_json = request.get_json(silent=True)
    request_args = request.args
    payload = json.loads(base64.b64decode(request_json['message']['data']))
    print("Message received")
    
    
    project_id = payload['incident']['resource']['labels']['project_id']
    zone = payload['incident']['resource']['labels']['zone']
    instance_name = payload['incident']['metric']['labels']['instance_name']
    notebook_path = f"projects/{project_id}/locations/{zone}/instances/{instance_name}"
        
    # Create a client
    client = np.NotebookServiceClient()

    # Initialize request argument(s)
    request = np.StopInstanceRequest(
    name=notebook_path,
    )

    # Make the request
    operation = client.stop_instance(request=request)

    print(f"Stopping notebook {notebook_path}..")

    response = operation.result()

    # Handle the response
    print(response)
    return 'Stopped', 200

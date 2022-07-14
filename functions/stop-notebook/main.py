import functions_framework
from google.cloud import notebooks_v1beta1 as np

@functions_framework.http
def stop_notebook(name):
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
    print(request_json)
    if request_json and 'name' in request_json:
        name = request_json['name']
    elif request_args and 'name' in request_args:
        name = request_args['name']
    else:
        name = 'not provided'
    
    # Create a client
    client = np.NotebookServiceClient()

    # Initialize request argument(s)
    request = np.StopInstanceRequest(
    name=name,
    )

    # Make the request
    operation = client.stop_instance(request=request)

    print("Waiting for operation to complete...")

    response = operation.result()

    # Handle the response
    print(response)
    return response

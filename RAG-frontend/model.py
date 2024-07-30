import requests

def model_response(message):
    # add the api endpoint 
    # url = "API"  # API endpoint its ususally an endpoint 
    # with the /prompt route from the backend
    # data = {"messages": [{"role": "user", "content": message}]}
    url = "123.123.123.123/prompt"  # API endpoint
    data = {"messages" : message}
    try:
        response = requests.post(url, json=data)  # Sending POST request
        return response.text  # Returning text response from the server
    except requests.exceptions.RequestException as e:  # Handle request exceptions
        return f"Error: {str(e)}"
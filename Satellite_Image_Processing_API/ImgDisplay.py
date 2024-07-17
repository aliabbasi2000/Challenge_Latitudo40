from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import os

# My client credentials
client_id = 'client_id'
client_secret = 'client_secret'

# Create a session
client = BackendApplicationClient(client_id=client_id)
oauth = OAuth2Session(client=client)

# Get token for the session
token = oauth.fetch_token(token_url='https://services.sentinel-hub.com/auth/realms/main/protocol/openid-connect/token',
                          client_secret=client_secret, include_client_id=True)

# All requests using this session will have an access token automatically added
resp = oauth.get("https://services.sentinel-hub.com/configuration/v1/wms/instances")


# Error Handling
def sentinelhub_compliance_hook(response):
    response.raise_for_status()
    return response

oauth.register_compliance_hook("access_token_response", sentinelhub_compliance_hook)



import requests

def request_and_handle(url):
    try:
        response = requests.get(url)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            print("Request successful")
            # You can handle the response data here, for example, saving it to a file
            with open("response_image.jpeg", "wb") as f:
                f.write(response.content)
            print("Response image saved as 'response_image.jpeg'")
        else:
            print(f"Request failed with status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")



# Replace '<your instance id>' with your actual instance id in the URL
url = "https://services.sentinel-hub.com/ogc/wms/a03e2b6c-8122-4daf-9e16-02f716b7c56c?REQUEST=GetMap&CRS=CRS:84&BBOX=7.65915,45.04249,7.702144,45.069835&LAYERS=NDVI&WIDTH=550&HEIGHT=495&FORMAT=image/jpeg&TIME=2024-03-20/2024-04-20"
request_and_handle(url)
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import os

# client credentials
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


# request part

import requests
import json

evalscript = """
//VERSION=3
function setup() {
  return {
    input: [{
      bands: [
        "B04",
        "B08",
        "SCL",
        "dataMask"
      ]
    }],
    output: [
      {
        id: "data",
        bands: 1
      },
      {
        id: "dataMask",
        bands: 1
      }]
  }
}

function evaluatePixel(samples) {
    let ndvi = (samples.B08 - samples.B04)/(samples.B08 + samples.B04)

    var validNDVIMask = 1
    if (samples.B08 + samples.B04 == 0 ){
        validNDVIMask = 0
    }

    var noWaterMask = 1
    if (samples.SCL == 6 ){
        noWaterMask = 0
    }

    return {
        data: [ndvi],
        // Exclude nodata pixels, pixels where ndvi is not defined and water pixels from statistics:
        dataMask: [samples.dataMask * validNDVIMask * noWaterMask]
    }
}
"""


stats_request = {
  "input": {
   "bounds": {
      "bbox": [
        7.65915,
        45.04249,
        7.702144,
        45.069835
      ] 
        ,
    "properties": {
        "crs": "http://www.opengis.net/def/crs/EPSG/0/32633"
        }
    },
    "data": [
      {
        "type": "sentinel-2-l2a",
        "dataFilter": {
            "mosaickingOrder": "leastCC"
        }
      }
    ]
  },
  "aggregation": {
    "timeRange": {
        "from": "2020-01-01T00:00:00Z",
        "to": "2020-12-31T00:00:00Z"
      },
    "aggregationInterval": {
        "of": "P30D"
    },
    "evalscript": evalscript,
    "resx": 10,
    "resy": 10
  }
}

headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json'
}

url = "https://services.sentinel-hub.com/api/v1/statistics"

response = oauth.request("POST", url=url, headers=headers, json=stats_request)
sh_statistics = response.json()
sh_statistics



if response == 200:
	print("Response = 200. Everything is OK!")

if response.status_code == 200:
    # Parse JSON response
    json_data = response.json()

    # Define the file path the current path of application
    file_name = "response1.json"  
    file_path = os.path.join(os.getcwd(), file_name)

    # Write JSON data to file
    with open(file_path, "w") as file:
        json.dump("Basic statistics of NDVI with water pixels excluded", file)
        json.dump(json_data, file, indent=4)

    print("JSON response saved successfully.")
    print("The results in JSON file contain statistics of NDVI with water pixels excluded (custom output dataMask)")
else:
    print("Error:", response.status_code)



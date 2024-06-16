from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

import requests
import json



# client credentials
client_id = '1d467a26-0ae1-4a19-b6ba-b89345b45ad9'
client_secret = '6z0JYR6NOHK8Sc0xVqAUAIjrCdKUlPZD'

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





url = "https://services.sentinel-hub.com/api/v1/statistics"
headers = {
  "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJ3dE9hV1o2aFJJeUowbGlsYXctcWd4NzlUdm1hX3ZKZlNuMW1WNm5HX0tVIn0.eyJleHAiOjE3MTM2NTA5NjUsImlhdCI6MTcxMzY0NzM2NSwiYXV0aF90aW1lIjoxNzEzNjQ3MzY0LCJqdGkiOiI2NGQ2OThmNC05MzMxLTQzYWUtOTE5Ny1jOGNhMDcwNTQzNzUiLCJpc3MiOiJodHRwczovL3NlcnZpY2VzLnNlbnRpbmVsLWh1Yi5jb20vYXV0aC9yZWFsbXMvbWFpbiIsInN1YiI6IjdiNjZlNDQxLTM1MWItNDgxZC1hMDU5LTg1NjA1ZDIyYTQ0ZCIsInR5cCI6IkJlYXJlciIsImF6cCI6IjBmNjFkMzg1LTVjOGItNDRmOS1hMTU0LTJhZGY1MWQ1MDE0MSIsIm5vbmNlIjoiZDNiOGJlOTUtYmZiOS00NTIzLThjNmItZTBjNjI0ZTZjOTQ0Iiwic2Vzc2lvbl9zdGF0ZSI6IjliMDA1YmFlLTFlZGItNGRmZC1hZTFhLTVmZjQxNjFlYTZhYSIsImFsbG93ZWQtb3JpZ2lucyI6WyJodHRwczovL2FwcHMuc2VudGluZWwtaHViLmNvbSJdLCJzY29wZSI6Im9wZW5pZCBlbWFpbCBwcm9maWxlIiwic2lkIjoiOWIwMDViYWUtMWVkYi00ZGZkLWFlMWEtNWZmNDE2MWVhNmFhIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsIm5hbWUiOiJBbGkgQWJiYXNpIiwicHJlZmVycmVkX3VzZXJuYW1lIjoiYWxpLmFiYmFzaTc5Nzk3OUBnbWFpbC5jb20iLCJnaXZlbl9uYW1lIjoiQWxpIiwiZmFtaWx5X25hbWUiOiJBYmJhc2kiLCJlbWFpbCI6ImFsaS5hYmJhc2k3OTc5NzlAZ21haWwuY29tIiwiYWNjb3VudCI6ImQ4ZGMxMGM3LWExODUtNDljZi05NmU4LWFhNmRlZGYyNTVmNSJ9.ON-VRx6fxibLwgykwPEsanRdn5kBpKGgCyjmDyp4L_0lPg4Kx6DmaDGWYeDw7mW7I1Smh5DBWALzlvlhopLBE0aMVII4YySO8__mttSY3gXpa7FwXtakXc4PKB5WAcrQcN-C4q2uuFwnnY7L9XMYPnxIAjqMAWwZ_6o_3HmaOGRMOl1kj3p9T8kIp6ONDIRfReHxHwBTDawgTRzQ_vupIZnH6r7P7_VEO796amVCQlbUKeTDLf54GFj1OVxu8TXmYFYZAg2tPMSQIfi770CabrrIFncRnGLCTbHca52zzBxG9DLCVKEKRkUKG1OJ7MDD2FO9yYl2Q93kpBqoEIjuxA",
  "Accept": "application/json",
  "Content-Type": "application/json"
}
data = {
  "input": {
    "bounds": {
      "bbox": [
        7.65915,
        45.04249,
        7.702144,
        45.069835
      ]
    },
    "data": [
      {
        "dataFilter": {},
        "type": "sentinel-2-l2a"
      }
    ]
  },
  "aggregation": {
    "timeRange": {
      "from": "2024-03-20T00:00:00Z",
      "to": "2024-04-20T23:59:59Z"
    },
    "aggregationInterval": {
      "of": "P10D"
    },
    "width": 512,
    "height": 460.869,
    "evalscript": "//VERSION=3\nfunction setup() {\n  return {\n    input: [{\n      bands: [\n        \"B04\",\n        \"B08\",\n        \"SCL\",\n        \"dataMask\"\n      ]\n    }],\n    output: [\n      {\n        id: \"data\",\n        bands: 3\n      },\n      {\n        id: \"scl\",\n        sampleType: \"INT8\",\n        bands: 1\n      },\n      {\n        id: \"dataMask\",\n        bands: 1\n      }]\n  };\n}\n\nfunction evaluatePixel(samples) {\n    let index = (samples.B08 - samples.B04) / (samples.B08+samples.B04);\n    return {\n        data: [index, samples.B08, samples.B04],\n        dataMask: [samples.dataMask],\n        scl: [samples.SCL]\n    };\n}\n"
  },
  "calculations": {
    "default": {}
  }
}

response = requests.post(url, headers=headers, json=data)




###########################################################################


if response == 200:
  print("Response = 200. Everything is OK!")

if response.status_code == 200:
    # Parse JSON response
    json_data = response.json()

    # Define the file path where you want to save the JSON file
    file_path = "C:/Users/ASUS/Desktop/SatelliteImgProcessing_withAPI/response5.json"

    # Write JSON data to file
    with open(file_path, "w") as file:
        json.dump(json_data, file)

    print("JSON response saved successfully.")
else:
    print("Error:", response.status_code)

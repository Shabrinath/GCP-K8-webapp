from flask import Flask, jsonify, request, json
import json, requests, strip
app = Flask(__name__)


@app.route("/")
@app.route("/home")
def home():
    return "<h1>Home Page</h1>"


@app.route('/kube', methods=['POST'])
def kube():
    responseFromDialogflow = request.get_json()
    response1 = json.dumps(responseFromDialogflow)
    response_json = json.loads(response1)
    for var in response_json['queryResult']['outputContexts']:
       clustername = var['parameters']['any']
       nodecount = var['parameters']['number']
       print clustername
       node_count = str(nodecount)
       print node_count
     
#NOTE: 'url' , 'Payload', 'Authorization' needs to be changed.
#You can get your payload and url from GCP console.
#For Auth-Token look at my other blog. 
       url = "https://container.googleapis.com/v1beta1/projects/project5-213120/zones/us-central1-a/clusters"

       payload = "{\r\n  \"cluster\": {\r\n    \"name\": \""+clustername+"\",\r\n    \"masterAuth\": {\r\n      \"username\": \"admin\",\r\n      \"clientCertificateConfig\": {\r\n        \"issueClientCertificate\": true\r\n      }\r\n    },\r\n    \"loggingService\": \"logging.googleapis.com\",\r\n    \"monitoringService\": \"monitoring.googleapis.com\",\r\n    \"network\": \"projects/project5-213120/global/networks/default\",\r\n    \"addonsConfig\": {\r\n      \"httpLoadBalancing\": {},\r\n      \"kubernetesDashboard\": {}\r\n    },\r\n    \"subnetwork\": \"projects/project5-213120/regions/us-central1/subnetworks/default\",\r\n    \"nodePools\": [\r\n      {\r\n        \"name\": \"default-pool\",\r\n        \"config\": {\r\n          \"machineType\": \"n1-standard-1\",\r\n          \"diskSizeGb\": 100,\r\n          \"oauthScopes\": [\r\n            \"https://www.googleapis.com/auth/compute\",\r\n            \"https://www.googleapis.com/auth/devstorage.read_only\",\r\n            \"https://www.googleapis.com/auth/logging.write\",\r\n            \"https://www.googleapis.com/auth/monitoring\",\r\n            \"https://www.googleapis.com/auth/servicecontrol\",\r\n            \"https://www.googleapis.com/auth/service.management.readonly\",\r\n            \"https://www.googleapis.com/auth/trace.append\"\r\n          ],\r\n          \"imageType\": \"COS\",\r\n          \"diskType\": \"pd-standard\"\r\n        },\r\n        \"initialNodeCount\": "+node_count+",\r\n        \"autoscaling\": {},\r\n        \"management\": {\r\n          \"autoRepair\": true\r\n        },\r\n        \"version\": \"1.9.7-gke.6\"\r\n      }\r\n    ],\r\n    \"networkPolicy\": {},\r\n    \"ipAllocationPolicy\": {},\r\n    \"masterAuthorizedNetworksConfig\": {},\r\n    \"privateClusterConfig\": {},\r\n    \"initialClusterVersion\": \"1.9.7-gke.6\",\r\n    \"location\": \"us-central1-a\"\r\n  }\r\n}"

       headers = {
    'Content-Type': "application/json",
    'Authorization': "Bearer ya29.GltEBrSshigzf2IZYvCfddmmjZYbVDfi1FlxkiUIpEsO3Zx9s1ydnFpbk7tYSogfGW4ptE0tPpBqzzgDaWBEUbw9jNh8F67uqzCUNtBeynS2-h8choPqksJ1aymp",
    'Cache-Control': "no-cache"
    }

       response = requests.request("POST", url, data=payload, headers=headers)

       print(response.text)

       return jsonify ({
             "payload": {
    "webhook": {
      "text": "Successfully deployed K8."
    }
  },
  "fulfillmentText": "your Kubernetes cluster is deployed!!!",
  "source": "webhook"
}), 201


if __name__ == '__main__':
    app.run(host="172.31.34.125", debug=True, port=8080)


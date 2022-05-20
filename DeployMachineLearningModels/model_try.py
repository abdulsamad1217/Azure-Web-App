import urllib.request
import json
import os
import ssl

def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.

# Request data goes here
data = {
  "data": [
    {
      "Application Type": 0,
      "Batch Enrolled": 0,
      "Collection 12 months Medical": 0,
      "Collection Recovery Fee": 0,
      "Debit to Income": 0,
      "Delinquency - two years": 0,
      "Employment Duration": 0,
      "Funded Amount": 0,
      "Funded Amount Investor": 0,
      "Grade": 0,
      "Home Ownership": 0,
      "Initial List Status": 0,
      "Inquires - six months": 0,
      "Interest Rate": 0,
      "Last week Pay": 0,
      "Loan Amount": 0,
      "Loan Title": 0,
      "Open Account": 0,
      "Public Record": 0,
      "Recoveries": 0,
      "Revolving Balance": 0,
      "Revolving Utilities": 0,
      "Sub Grade": 0,
      "Term": 0,
      "Total Accounts": 0,
      "Total Collection Amount": 0,
      "Total Current Balance": 0,
      "Total Received Interest": 0,
      "Total Received Late Fee": 0,
      "Total Revolving Credit Limit": 0,
      "Verification Status": 0
    }
  ],
  "method": "predict"
}

body = str.encode(json.dumps(data))

url = 'http://20.221.6.249:80/api/v1/service/aks-service/score'
api_key = os.environ.get('CCProject')    # Replace this with the API key for the web service
headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

req = urllib.request.Request(url, body, headers)

try:
    response = urllib.request.urlopen(req)

    result = response.read()
    print(result)
except urllib.error.HTTPError as error:
    print("The request failed with status code: " + str(error.code))

    # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
    print(error.info())
    print(json.loads(error.read().decode("utf8", 'ignore')))
import pandas as pd
import random
import urllib.request
import json
import os
import ssl
import numpy as np

df = pd.read_csv("F:/Cloud Computing/Azure_Project-main/train.csv")
drop_elements = ['ID', 'Accounts Delinquent', 'Payment Plan','Loan Status']
df = df.drop(drop_elements, axis = 1)

columns_name_temp = df.columns
column_names = columns_name_temp.tolist()

features = [17120,10365,16025.08269,59,2575549,12.16392574,1,41,2,
            12.16392574,2,1,16.74921941,1,0,12,1,3576,67.27828675,5,
            1,4469.449851,1,8,1,0,0,135,24,475442,4364]        
        #[x for x in request.form.values()]

final_features = [np.array(features)]
final_features_df=pd.DataFrame(final_features,columns=column_names)
print(int(final_features_df["Collection 12 months Medical"][0]))



data = {
  "data": [
    {
      "Application Type": int(final_features_df["Application Type"][0]),
      "Batch Enrolled": int(final_features_df["Batch Enrolled"][0]),
      "Collection 12 months Medical": int(final_features_df["Collection 12 months Medical"][0]),
      "Collection Recovery Fee": final_features_df["Collection Recovery Fee"][0],
      "Debit to Income": final_features_df["Debit to Income"][0],
      "Delinquency - two years": int(final_features_df["Delinquency - two years"][0]),
      "Employment Duration": int(final_features_df["Employment Duration"][0]),
      "Funded Amount": int(final_features_df["Funded Amount"][0]),
      "Funded Amount Investor": final_features_df["Funded Amount Investor"][0],
      "Grade": int(final_features_df["Grade"][0]),
      "Home Ownership": final_features_df["Home Ownership"][0],
      "Initial List Status": int(final_features_df["Initial List Status"][0]),
      "Inquires - six months": int(final_features_df["Inquires - six months"][0]),
      "Interest Rate": final_features_df["Interest Rate"][0],
      "Last week Pay": int(final_features_df["Last week Pay"][0]),
      "Loan Amount": int(final_features_df["Loan Amount"][0]),
      "Loan Title": int(final_features_df["Loan Title"][0]),
      "Open Account": int(final_features_df["Open Account"][0]),
      "Public Record": int(final_features_df["Public Record"][0]),
      "Recoveries": final_features_df["Recoveries"][0],
      "Revolving Balance": int(final_features_df["Revolving Balance"][0]),
      "Revolving Utilities": final_features_df["Revolving Utilities"][0],
      "Sub Grade": int(final_features_df["Sub Grade"][0]),
      "Term": int(final_features_df["Term"][0]),
      "Total Accounts": int(final_features_df["Total Accounts"][0]),
      "Total Collection Amount": int(final_features_df["Total Collection Amount"][0]),
      "Total Current Balance": int(final_features_df["Total Current Balance"][0]),
      "Total Received Interest": final_features_df["Total Received Interest"][0],
      "Total Received Late Fee": final_features_df["Total Received Late Fee"][0],
      "Total Revolving Credit Limit": int(final_features_df["Total Revolving Credit Limit"][0]),
      "Verification Status": int(final_features_df["Verification Status"][0])
    }
  ],
  "method": "predict"
}


def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.

body = str.encode(json.dumps(data))

url = 'http://20.221.6.249:80/api/v1/service/aks-service/score'
api_key = 'mwmzRYDjqHMdTIO5H1xoBIVA24nVy4FZ'    # Replace this with the API key for the web service
headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

req = urllib.request.Request(url, body, headers)

try:
    response = urllib.request.urlopen(req)

    result = response.read()
    print(result)
    prediction= json.loads(json.loads(result))["result"][0]
    print(prediction)

except urllib.error.HTTPError as error:
    print("The request failed with status code: " + str(error.code))

    # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
    print(error.info())
    print(json.loads(error.read().decode("utf8", 'ignore')))


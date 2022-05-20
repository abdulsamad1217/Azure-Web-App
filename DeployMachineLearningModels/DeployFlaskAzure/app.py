import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template
import urllib.request
import json
import os
import ssl

app = Flask(__name__,template_folder='templates')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    df = pd.read_csv("F:/Cloud Computing/Azure_Project-main/train.csv")
    drop_elements = ['ID', 'Accounts Delinquent', 'Payment Plan','Loan Status']
    df = df.drop(drop_elements, axis = 1)

    columns_name_temp = df.columns
    column_names = columns_name_temp.tolist()

    features = [x for x in request.form.values()]

    final_features = [np.array(features)]
    final_features_df=pd.DataFrame(final_features,columns=column_names)

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

    url = 'http://a8c9227a-44da-4a87-95bc-879e2597f8da.eastus.azurecontainer.io/score'
    api_key = 'mwmzRYDjqHMdTIO5H1xoBIVA24nVy4FZ'    # Replace this with the API key for the web service...
    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)

        result = response.read()
        prediction= json.loads(json.loads(result))["result"][0]
        if prediction == 0:
            return render_template('index.html', prediction_text='Not Eligible for the loan... Sorry')
        elif prediction == 1:
            return render_template('index.html', prediction_text='Eligible for the loan... Congrats')
        else:
            return render_template('index.html', prediction_text="Can not process at the movement... Please try again")
    except urllib.error.HTTPError as error:
        return render_template('index.html', prediction_text="Something Went wrong... Please Contact Customer service")
       


if __name__ == '__main__':
	app.run(host='0.0.0.0')

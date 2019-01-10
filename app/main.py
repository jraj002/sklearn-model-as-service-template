from flask import Flask
from flask import json
from flask import request
from flask import jsonify
import traceback
import pandas as pd
from sklearn.externals import joblib

clf = joblib.load('titanic.pkl')
features = ["Sex","Pclass","SibSp","Age"]

app = Flask(__name__)

@app.route("/")
def hello():
    return "Home Page For Titanic Survival Prediction"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        json_request = request.get_json(silent=True)
        print(json_request)
        print(type(json_request))
        req_df = pd.DataFrame([json_request])
        print(req_df)


        prediction = clf.predict(X = req_df[features])
        return jsonify(model_version=23,result=prediction.tolist()[0])

    except Exception:
        return jsonify({'error': 'exception', 'trace': traceback.format_exc()})

@app.route('/hello')
def api_hello():
    if 'name' in request.args:
        return 'Hello ' + request.args['name']
    else:
        return 'Hello John Doe'

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=80)

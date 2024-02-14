from flask import Flask, request, jsonify
from numpy import array
from joblib import load
from json import loads

app = Flask(__name__)
model = load('model.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    data = loads(request.get_json())
    features = [
        data['pH'], data['Soil EC'], data['Phosphorus'],
        data['Potassium'], data['Urea'], data['T.S.P'],
        data['M.O.P'], data['Temperature'], data['Plant Type']
    ]

    prediction = model.predict(array(features).reshape(1, -1))

    return jsonify({'moisture_prediction': prediction.tolist()})
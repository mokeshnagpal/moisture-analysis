from flask import Flask, request, jsonify
import numpy as np
import joblib

app = Flask(__name__)
model = joblib.load('model.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    prediction = model.predict(np.array(data['pH'], data['Soil EC'], data['Phosphorus'], data['Potassium'], data['Urea'], data['T.S.P'], data['M.O.P'], data['Temperature'], data['Plant Type']).reshape(1, -1))

    return jsonify({'moisture_prediction': prediction.tolist()})

if __name__ == '__main__':
    app.run(debug=True)
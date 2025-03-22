from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
import numpy as np
import pickle
import os

# Load environment variables
load_dotenv()

# Get the frontend URL from environment variables
FRONTEND_URL = os.getenv('FRONTEND_URL') 

# Create flask app
app = Flask(__name__)
from flask_cors import CORS

CORS(app)
# CORS(app, origins=['http://localhost:5173', FRONTEND_URL])


model = pickle.load(open("model.pkl", "rb"))

# @app.route("/")
# def Home():
#     return render_template("index.ejs")

# @app.route("/predict", methods=["POST"])
# def predict():
#     # Handles form submissions from the EJS frontend
#     float_features = [float(x) for x in request.form.values()]
#     features = [np.array(float_features)]
#     prediction = model.predict(features)
#     return render_template("index.ejs", prediction_text=f"The Predicted Crop is {prediction[0]}")

@app.route("/api/predict", methods=["POST"])
def api_predict():
    try:
        print(f"Request Content-Type: {request.content_type}")
        print(f"Request Data: {request.data}")
        print(f"Request Form: {request.form}")

        # Handle JSON data
        if request.is_json:
            data = request.get_json(force=True)
            float_features = [
                float(data['Nitrogen']),
                float(data['Phosphorus']),
                float(data['Potassium']),
                float(data['temperature']),
                float(data['humidity']),
                float(data['pH']),
                float(data['rainfall']),
            ]
        # Handle form-data
        elif request.form:
            float_features = [
                float(request.form.get('Nitrogen', 0)),
                float(request.form.get('Phosphorus', 0)),
                float(request.form.get('Potassium', 0)),
                float(request.form.get('temperature', 0)),
                float(request.form.get('humidity', 0)),
                float(request.form.get('pH', 0)),
                float(request.form.get('rainfall', 0)),
            ]
        else:
            return jsonify({'error': 'Unsupported Media Type. Use JSON or form-data.'}), 415

        # Prepare features and make a prediction
        features = [np.array(float_features)]
        prediction = model.predict(features)
        return jsonify({'prediction': prediction[0]})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)

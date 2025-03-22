from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import numpy as np
import pickle
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure CORS to allow requests from the frontend URL
FRONTEND_URL = os.getenv('FRONTEND_URL', '*')
CORS(app, resources={r"/*": {"origins": FRONTEND_URL}})

# Load the model
model_path = os.path.join(os.path.dirname(__file__), 'model.pkl')
if not os.path.isfile(model_path):
    raise FileNotFoundError(f"Model file not found at {model_path}")

model = pickle.load(open(model_path, "rb"))

@app.route("/", methods=["GET"])
def home():
    return jsonify({'msg': 'This is the home page'})

@app.route("/api/predict", methods=["POST"])
def predict():
    try:
        print(f"Request Content-Type: {request.content_type}")
        print(f"Request Data: {request.data}")

        # Handle JSON data
        if request.is_json:
            data = request.get_json(force=True)
            float_features = [
                float(data.get('Nitrogen', 0)),
                float(data.get('Phosphorus', 0)),
                float(data.get('Potassium', 0)),
                float(data.get('temperature', 0)),
                float(data.get('humidity', 0)),
                float(data.get('pH', 0)),
                float(data.get('rainfall', 0)),
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

        # Make a prediction
        features = [np.array(float_features)]
        prediction = model.predict(features)
        return jsonify({'prediction': prediction[0]})

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import pickle
import os

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Get the frontend URL from environment variables
FRONTEND_URL = os.getenv('FRONTEND_URL')

# Create flask app
app = Flask(__name__)

# Configure CORS to allow requests from frontend
CORS(app, resources={r"/*": {"origins": [FRONTEND_URL]}})

# Load the model
model_path = os.path.join(os.path.dirname(__file__), 'model.pkl')
model = pickle.load(open(model_path, "rb"))

@app.route("/api/predict", methods=["POST"])
def api_predict():
    try:
        # Check if data is JSON
        if request.is_json:
            data = request.get_json()
        else:
            return jsonify({'error': 'Invalid request format. Use JSON.'}), 400

        # Extract and validate data
        required_fields = ['Nitrogen', 'Phosphorus', 'Potassium', 'temperature', 'humidity', 'pH', 'rainfall']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing fields in input data'}), 400

        float_features = [float(data[field]) for field in required_fields]
        features = [np.array(float_features)]

        # Make prediction
        prediction = model.predict(features)
        return jsonify({'prediction': prediction[0]})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Health check route
@app.route("/api/health")
def health_check():
    return jsonify({"status": "healthy"})

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

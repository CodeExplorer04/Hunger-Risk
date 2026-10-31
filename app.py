import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import numpy as np
import joblib

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Safely resolve model paths relative to this script
model_path = os.path.join(BASE_DIR, "hunger_model.pkl")
scaler_path = os.path.join(BASE_DIR, "scaler.pkl")
le_path = os.path.join(BASE_DIR, "label_encoder.pkl")

model = None
scaler = None
le = None

if os.path.exists(model_path) and os.path.exists(scaler_path) and os.path.exists(le_path):
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    le = joblib.load(le_path)
    print("✅ Hunger project ML models loaded successfully!")
else:
    print("⚠️ Warning: Model pkl files not found. Run train_model.py first.")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    global model, scaler, le
    data = request.json or {}

    try:
        if model is None or scaler is None or le is None:
            return jsonify({"prediction": "Model uninitialized. Please run train_model.py"}), 500

        rank = float(data.get("rank", 50))
        y2000 = float(data.get("y2000", 25))
        y2008 = float(data.get("y2008", 22))
        y2015 = float(data.get("y2015", 18))
        y2023 = float(data.get("y2023", 15))

        features = np.array([[rank, y2000, y2008, y2015, y2023]])
        scaled = scaler.transform(features)
        pred = model.predict(scaled)
        result = le.inverse_transform(pred)[0]

        # Calculate hunger trend
        trend = "Improving" if y2023 < y2000 else "Deteriorating"

        return jsonify({
            "prediction": str(result),
            "trend": trend,
            "y2023": y2023,
            "status": "success"
        })

    except Exception as e:
        return jsonify({"prediction": f"Error: {str(e)}"}), 400


if __name__ == "__main__":
    app.run(debug=True, port=5000)

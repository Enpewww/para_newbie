from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
# import tensorflow as tf
# import pickle

app = Flask(__name__)

# Load models here (mocking for now)
# model = tf.keras.models.load_model('model.h5')
# scaler = pickle.load(open('scaler.pkl', 'rb'))

@app.route('/predict_tier', methods=['POST'])
def predict_tier():
    try:
        data = request.json
        # Example input: {"income": 5000000, "expense": 3000000, "cashflow": 2000000}
        
        # Mock Logic for Tiering
        # In real implementation, use the loaded model
        cashflow = data.get('cashflow', 0)
        
        if cashflow > 10000000:
            tier = 'Gold'
        elif cashflow > 5000000:
            tier = 'Silver'
        else:
            tier = 'Bronze'
            
        return jsonify({
            "tier": tier,
            "score": 0.85, # Mock score
            "recommendation": f"Maintain positive cashflow to upgrade from {tier}."
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

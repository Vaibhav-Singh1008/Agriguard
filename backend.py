from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, Plan, seed_db
import os
import io
import numpy as np
from PIL import Image
import tensorflow as tf
from openai import OpenAI
from dotenv import load_dotenv
import hashlib
import base64
import json
import requests
import uuid

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Database Configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'agriguard.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Initialize OpenAI
client = OpenAI()

# Load TensorFlow Model
MODEL_PATH = os.path.join(basedir, 'crop_disease_model.h5')
try:
    model = tf.keras.models.load_model(MODEL_PATH)
    print("TensorFlow model loaded successfully.")
except Exception as e:
    print(f"Warning: Could not load TF model. Error: {e}")
    model = None

CLASS_NAMES = [
    "Healthy Crop - No action needed",
    "Leaf Blight - Apply Copper Fungicide",
    "Nitrogen Deficiency - Apply Urea",
    "Rust - Apply appropriate fungicide"
]

with app.app_context():
    db.create_all()
    seed_db()

# --- ROUTES ---

@app.route('/api/diagnose', methods=['POST'])
def diagnose_crop():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400
    
    file = request.files['image']
    
    if model is None:
        return jsonify({"error": "AI Model is currently offline."}), 503

    try:
        image_bytes = file.read()
        img = Image.open(io.BytesIO(image_bytes)).resize((224, 224)) 
        img_array = np.array(img) / 255.0 
        img_array = np.expand_dims(img_array, axis=0) 
        
        predictions = model.predict(img_array)
        predicted_class_index = np.argmax(predictions[0])
        confidence = float(np.max(predictions[0]))
        
        return jsonify({
            "diagnosis": CLASS_NAMES[predicted_class_index], 
            "confidence": f"{confidence * 100:.2f}%",
            "status": "success"
        })
    except Exception as e:
        print(f"Prediction Error: {e}")
        return jsonify({"error": "Failed to process the image."}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({"reply": "Please ask a question."}), 400

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are Agri-Guard, a knowledgeable AI assistant for farmers in India. Keep answers concise, practical, and empathetic."},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7
        )
        return jsonify({"reply": response.choices[0].message.content})
    except Exception as e:
        print(f"OpenAI API Error: {e}")
        return jsonify({"reply": "Trouble connecting to the AI database right now. Please try again."}), 500

@app.route('/api/plans', methods=['GET'])
def get_plans():
    plans = Plan.query.all()
    result = {}
    for plan in plans:
        if plan.category not in result:
            result[plan.category] = []
        result[plan.category].append({"id": plan.id, "name": plan.name, "price": plan.price})
    return jsonify(result)

@app.route('/api/checkout', methods=['POST'])
def checkout():
    data = request.json
    plan_id = data.get('plan_id')
    plan = Plan.query.get(plan_id)
    
    if not plan:
        return jsonify({"error": "Plan not found"}), 404

    merchant_id = os.getenv("PHONEPE_MERCHANT_ID", "PGTESTPAYUAT")
    salt_key = os.getenv("PHONEPE_SALT_KEY", "099eb0cd-02cf-4e2a-8aca-3e6c6aff0399")
    salt_index = os.getenv("PHONEPE_SALT_INDEX", "1")
    
    transaction_id = "TXN" + str(uuid.uuid4().hex)[:16].upper()
    amount_in_paise = plan.price * 100 
    
    payload = {
        "merchantId": merchant_id,
        "merchantTransactionId": transaction_id,
        "merchantUserId": "USER_FARMER_01",
        "amount": amount_in_paise,
        "redirectUrl": "http://localhost:3000/payment-success",
        "redirectMode": "REDIRECT",
        "callbackUrl": "http://localhost:5000/api/payment/callback",
        "paymentInstrument": {"type": "PAY_PAGE"}
    }
    
    base64_payload = base64.b64encode(json.dumps(payload).encode('utf-8')).decode('utf-8')
    string_to_hash = base64_payload + "/pg/v1/pay" + salt_key
    x_verify = hashlib.sha256(string_to_hash.encode('utf-8')).hexdigest() + "###" + salt_index
    
    headers = {"Content-Type": "application/json", "X-VERIFY": x_verify, "accept": "application/json"}
    phonepe_url = "https://api-preprod.phonepe.com/apis/pg-sandbox/pg/v1/pay"
    
    try:
        response = requests.post(phonepe_url, json={"request": base64_payload}, headers=headers)
        response_data = response.json()
        if response_data.get('success'):
            payment_url = response_data['data']['instrumentResponse']['redirectInfo']['url']
            return jsonify({"payment_url": payment_url, "transaction_id": transaction_id})
        else:
            return jsonify({"error": "Payment initiation failed"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/payment/callback', methods=['POST'])
def payment_callback():
    print("PhonePe Webhook Received:", request.json)
    return jsonify({"status": "Callback Received"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)

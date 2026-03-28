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

load_dotenv()

app = Flask(__name__)
CORS(app)

#Database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'agriguard.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

#OpenAI
client = OpenAI()

#TensorFlow Model
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

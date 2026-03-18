from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
db = SQLAlchemy(app)

class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_path = db.Column(db.String(200), nullable=False)
    prediction = db.Column(db.String(100))
    confidence = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()
    print("Database ban gaya!")

@app.route('/add')
def add_data():
    new_prediction = Prediction(
        image_path="cat.jpg",
        prediction="Cat",
        confidence=0.95
    )
    db.session.add(new_prediction)
    db.session.commit()
    return "Data add ho gaya!"

@app.route('/show')
def show_data():
    all_data = Prediction.query.all()
    result = ""
    for item in all_data:
        result += f"ID: {item.id} | Image: {item.image_path} | Result: {item.prediction} <br>"
    return result



# 3.Data DELETE 
@app.route('/delete/<int:id>')
def delete_data(id):
    record = Prediction.query.get(id)
    if record:
        db.session.delete(record)
        db.session.commit()
        return f"ID {id} delete ho gya!"
    return "record nahi mila!"

# /predict- AI result save 
@app.route('/predict',  methods =['post'])
def save_prediction():
    data = request.get_json()
    new_entry = prediction(
        image_path = data['image_path'],
        prediction =  data['prediction'],
        confidence = data['confidence']
    )
    db.session.add(new_entry)
    db.session.commit()
    return jsonify({"message" : "saved!", "id" : new_entry.id})

# /history
@app.route('/history', methods=['GET'])
def get_history():
    all_data = Prediction.query.all()
    result = []
    for item in all_data:
        result.append({
            "id": item.id,
            "image_path": item.image_path,
            "prediction": item.prediction,
            "confidence": item.confidence,
            "timestamp": str(item.timestamp)

        })
    return jsonify(result)
    
if __name__ == '__main__':
    app.run(debug=True)
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Plan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Integer, nullable=False) # Price in INR

def seed_db():
    if Plan.query.count() == 0:
        plans = [
            Plan(category='Grains', name='Wheat', price=500),
            Plan(category='Grains', name='Rice', price=500),
            Plan(category='Grains', name='Maize', price=700),
            Plan(category='Grains', name='Millets', price=850),
            Plan(category='Fruits', name='Orange', price=400),
            Plan(category='Fruits', name='Apple', price=400),
            Plan(category='Fruits', name='Bananas', price=500),
            Plan(category='Fruits', name='Pineapple', price=750),
            Plan(category='Vegetables', name='Onion', price=300),
            Plan(category='Vegetables', name='Brinjal', price=400),
            Plan(category='Vegetables', name='Pumpkin', price=400),
        ]
        db.session.bulk_save_objects(plans)
        db.session.commit() 

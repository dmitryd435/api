import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
import uuid
from datetime import datetime

app = Flask(__name__)

db_user = os.getenv('POSTGRES_USER')
db_password = os.getenv('POSTGRES_PASSWORD')
db_name = os.getenv('POSTGRES_DB')
db_host = 'postgres'

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{db_host}:5432/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Prometheus metrics
REQUEST_COUNT = Counter('request_count', 'Total Request Count', ['method', 'endpoint'])

class Transaction(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    payment_amount = db.Column(db.Float)
    coffee_type = db.Column(db.String(50))

    def __init__(self, payment_amount, coffee_type):
        self.payment_amount = payment_amount
        self.coffee_type = coffee_type

@app.before_request
def before_request():
    REQUEST_COUNT.labels(method=request.method, endpoint=request.path).inc()

@app.route('/buy_coffee', methods=['POST'])
def buy_coffee():
    data = request.get_json()
    payment_amount = data.get('payment_amount')
    
    if payment_amount < 2.00:
        coffee_type = "Espresso"
    elif 2.00 <= payment_amount < 3.00:
        coffee_type = "Latte"
    else:
        coffee_type = "Cappuccino"
    
    transaction = Transaction(payment_amount=payment_amount, coffee_type=coffee_type)
    db.session.add(transaction)
    db.session.commit()

    return jsonify({'coffee_type': coffee_type})

@app.route('/metrics', methods=['GET'])
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0', port=5000)

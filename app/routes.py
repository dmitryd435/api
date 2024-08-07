from flask import request, jsonify
from . import app, db, REQUEST_COUNT, REQUEST_LATENCY
from .models import Transaction
import time

@app.route('/buy_coffee', methods=['POST'])
@REQUEST_LATENCY.time()
def buy_coffee():
    start_time = time.time()
    REQUEST_COUNT.labels('coffee_api', '/buy_coffee').inc()
    
    data = request.get_json()
    payment = data.get('payment_amount')

    if payment < 2.00:
        coffee_type = "Espresso"
    elif 2.00 <= payment < 3.00:
        coffee_type = "Latte"
    else:
        coffee_type = "Cappuccino"

    transaction = Transaction(payment_amount=payment, coffee_type=coffee_type)
    db.session.add(transaction)
    db.session.commit()

    response = jsonify({
        'transaction_id': transaction.id,
        'timestamp': transaction.timestamp,
        'payment_amount': payment,
        'coffee_type': coffee_type
    })
    
    return response, 200

@app.route('/metrics', methods=['GET'])
def metrics():
    return generate_latest(), 200

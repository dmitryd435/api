from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import uuid
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{db_host}:5432/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Transaction(db.Model):
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()), unique=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    payment_amount = db.Column(db.Numeric, nullable=False)
    coffee_type = db.Column(db.String, nullable=False)

@app.route('/buy_coffee', methods=['POST'])
def buy_coffee():
    try:
        data = request.get_json()
        payment_amount = float(data.get('payment_amount', 0))

        if payment_amount < 2.00:
            coffee_type = "Espresso"
        elif 2.00 <= payment_amount < 3.00:
            coffee_type = "Latte"
        else:
            coffee_type = "Cappuccino"

        transaction = Transaction(
            id=str(uuid.uuid4()),  # Ensure a new UUID is generated
            timestamp=datetime.utcnow(),
            payment_amount=payment_amount,
            coffee_type=coffee_type
        )
        db.session.add(transaction)
        db.session.commit()

        return jsonify({"coffee_type": coffee_type}), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

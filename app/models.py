from . import db
from datetime import datetime
import uuid

class Transaction(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    payment_amount = db.Column(db.Float, nullable=False)
    coffee_type = db.Column(db.String(50), nullable=False)

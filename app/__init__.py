from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from prometheus_client import Counter, generate_latest, Summary

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@db:5432/coffee'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

REQUEST_COUNT = Counter('request_count', 'App Request Count', ['app_name', 'endpoint'])
REQUEST_LATENCY = Summary('request_latency_seconds', 'Request latency')

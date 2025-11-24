from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class SensorLog(db.Model):
    __tablename__ = "sensor_log"

    id = db.Column(db.Integer, primary_key=True)
    temperature_c = db.Column(db.Float)
    temperature_f = db.Column(db.Float)
    humidity = db.Column(db.Float)
    light = db.Column(db.Boolean)
    motion = db.Column(db.Boolean)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

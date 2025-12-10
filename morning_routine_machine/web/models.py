from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

db = SQLAlchemy()

class SensorLog(db.Model):
    __tablename__ = "sensor_log"

    id = db.Column(db.Integer, primary_key=True)
    temperature_c = db.Column(db.Float)
    temperature_f = db.Column(db.Float)
    humidity = db.Column(db.Float)
    light = db.Column(db.Boolean)
    motion = db.Column(db.Boolean)

    # ✅ Store UTC in the database (this is what already works)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def az_time(self):
        """
        Return this log's timestamp converted from UTC to Arizona time (UTC-7).
        If timestamp is None, return None.
        """
        if self.timestamp is None:
            return None
        # Arizona is UTC-7 year-round (no DST)
        return self.timestamp - timedelta(hours=7)

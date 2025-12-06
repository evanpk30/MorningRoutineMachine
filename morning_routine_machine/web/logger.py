# web/logger.py
from datetime import datetime

from web.models import db, SensorLog
from web.app import app   # import the Flask app so we can use its context


def log_sensor(temp_c, temp_f, humidity, light, motion):
    """
    Log one sensor reading into the SensorLog table.
    Safe to call from the automation script (separate process).
    """
    with app.app_context():
        # Make sure tables (including sensor_log) exist in THIS process
        db.create_all()

        entry = SensorLog(
            temperature_c=temp_c,
            temperature_f=temp_f,
            humidity=humidity,
            light=bool(light),
            motion=bool(motion),
            timestamp=datetime.utcnow(),
        )

        db.session.add(entry)
        db.session.commit()
        print(f"[DEBUG] Logged SensorLog row (id={entry.id})")

from flask import Flask
from web.models import db, SensorLog
import os

app = Flask(__name__, instance_relative_config=False)

# Absolute path to the correct DB location
DB_PATH = "/home/eklaasen/morning_routine_machine/web/instance/db.sqlite3"

# Ensure instance folder exists
os.makedirs("/home/eklaasen/morning_routine_machine/web/instance", exist_ok=True)

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

def log_sensor(temp_c, temp_f, humidity, light, motion):
    with app.app_context():
        entry = SensorLog(
            temperature_c=temp_c,
            temperature_f=temp_f,
            humidity=humidity,
            light=light,
            motion=motion
        )
        db.session.add(entry)
        db.session.commit()

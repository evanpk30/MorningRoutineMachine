from flask import Flask, render_template
from models import db, SensorLog   # models.py is in the same folder
import os

# Create the Flask app, using the instance/ folder for the DB
app = Flask(__name__, instance_relative_config=True)

# Make sure instance/ exists
os.makedirs(app.instance_path, exist_ok=True)

# SQLite DB in instance/db.sqlite3
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


@app.route("/")
def dashboard():
    # Query latest 50 rows
    logs = SensorLog.query.order_by(SensorLog.timestamp.desc()).limit(50).all()
    print(f"[DEBUG] Loaded {len(logs)} rows from SensorLog")
    return render_template("dashboard.html", logs=logs)


if __name__ == "__main__":
    with app.app_context():
        db_path = os.path.join(app.instance_path, "db.sqlite3")
        if not os.path.exists(db_path):
            print("Creating new database inside instance folder...")
            db.create_all()
        else:
            print("Database already exists, skipping create_all().")

    print("Starting Flask app on 0.0.0.0:5000 ...")
    app.run(host="0.0.0.0", port=5000)

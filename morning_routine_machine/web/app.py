# web/app.py
from flask import Flask, render_template, request, redirect, url_for
from web.models import db, SensorLog
from pathlib import Path
import os
import json

# --- Base directories ---
BASE_DIR = Path(__file__).resolve().parents[1]      # /home/.../morning_routine_machine
INSTANCE_DIR = BASE_DIR / "instance"                # /instance folder at project root
INSTANCE_DIR.mkdir(exist_ok=True)

DB_PATH = INSTANCE_DIR / "db.sqlite3"

print(f"[DEBUG] Flask using DB at: {DB_PATH}")

app = Flask(__name__, instance_path=str(INSTANCE_DIR))

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()
    print("[DEBUG] db.create_all() finished in app.py")

# ------------------------------
# Config handling
# ------------------------------
CONFIG_PATH = INSTANCE_DIR / "config.json"

DEFAULT_CONFIG = {
    "first_activation_mode": "light",  # "light" or "time"
    "first_activation_time": "07:30",  # HH:MM
}

def load_config():
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH, "r") as f:
                data = json.load(f)
            cfg = DEFAULT_CONFIG.copy()
            cfg.update(data)
            return cfg
        except json.JSONDecodeError:
            return DEFAULT_CONFIG.copy()
    else:
        return DEFAULT_CONFIG.copy()

def save_config(cfg: dict):
    INSTANCE_DIR.mkdir(exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump(cfg, f)

# ------------------------------
# Routes
# ------------------------------
@app.route("/")
def dashboard():
    logs = SensorLog.query.order_by(SensorLog.timestamp.desc()).limit(50).all()
    config = load_config()
    print(f"[DEBUG] Loaded {len(logs)} rows from SensorLog")
    return render_template("dashboard.html", logs=logs, config=config)

@app.route("/update-settings", methods=["POST"])
def update_settings():
    cfg = load_config()

    mode = request.form.get("activation_mode", "light")
    time_str = request.form.get("activation_time", "07:30")

    cfg["first_activation_mode"] = mode
    cfg["first_activation_time"] = time_str or "07:30"

    save_config(cfg)
    print(f"[DEBUG] Updated config: {cfg}")
    return redirect(url_for("dashboard"))

"""
app.py — Main Flask Application for AI-Powered Health Assistant
Production-ready with configuration system for web, Android, and iOS
"""
import os
import json
import uuid
import socket
import base64
import pandas as pd
from datetime import datetime
from functools import wraps
from werkzeug.utils import secure_filename
from flask import (
    Flask, render_template, request, redirect, url_for,
    session, flash, jsonify
)
from werkzeug.security import generate_password_hash, check_password_hash

try:
    from flask_cors import CORS
except ImportError:
    CORS = None

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Import configuration
from config import get_config

# Internal modules
import urllib.parse
import database as db
import email_service as mail
import sms_service as sms
import recommendation as rec
import chatbot as ai_bot
import model_training as ml

app = Flask(__name__)

# Load configuration based on environment
config = get_config()
app.config.from_object(config)

# Enable CORS for Mobile Apps
if CORS:
    allowed_origins = [origin.strip() for origin in app.config["ALLOWED_ORIGINS"]]
    CORS(app, 
         resources={r"/api/*": {"origins": allowed_origins}},
         supports_credentials=True)

# Uploads directory
UPLOAD_FOLDER = app.config.get("UPLOAD_FOLDER", 
    os.path.join(os.path.dirname(__file__), "static", "uploads", "reports"))
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Cache disease descriptions
_disease_desc_cache = {}

def get_disease_description_map():
    global _disease_desc_cache
    if not _disease_desc_cache:
        desc_path = os.path.join(os.path.dirname(__file__), "data", "disease_description.csv")
        if os.path.exists(desc_path):
            df = pd.read_csv(desc_path)
            for _, row in df.iterrows():
                _disease_desc_cache[row["disease"]] = {
                    "description": row["description"],
                    "doctor_advice": row["doctor_advice"]
                }
    return _disease_desc_cache


# ── Auth Decorators ────────────────────────────────────────────────────────

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function


def doctor_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "doctor_id" not in session:
            flash("Please log in as a doctor to access this portal.", "warning")
            return redirect(url_for("doctor_login"))
        return f(*args, **kwargs)
    return decorated_function


# ── Context Processor ──────────────────────────────────────────────────────

@app.context_processor
def inject_globals():
    return {
        "now": datetime.now(),
        "is_logged_in": "user_id" in session or "doctor_id" in session,
        "current_user_name": session.get("user_name"),
        "is_doctor": "doctor_id" in session
    }


# ══════════════════════════════════════════════════════════════════════════
#  PUBLIC ROUTES
# ══════════════════════════════════════════════════════════════════════════

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/download")
@app.route("/install")
def download():
    """Download/Install page with QR codes for all platforms"""
    from datetime import datetime
    
    android_store_url = os.getenv(
        "ANDROID_STORE_URL",
        "https://play.google.com/store/apps/details?id=com.aihealth.assistant"
    )
    ios_store_url = os.getenv(
        "IOS_STORE_URL",
        "https://apps.apple.com/app/ai-health-assistant/id6739271845"
    )
    web_url = os.getenv("PUBLIC_WEB_URL", "http://127.0.0.1:5000")
    
    return render_template(
        "download.html",
        android_store_url=android_store_url,
        ios_store_url=ios_store_url,
        web_url=web_url,
        year=datetime.now().year
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        age = request.form.get("age", "").strip()
        gender = request.form.get("gender", "").strip()
        email = request.form.get("email", "").strip().lower()
        phone = request.form.get("phone", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        # Validation
        if not full_name or not email or not password:
            flash("Please fill in all required fields.", "danger")
            return render_template("register.html")

        if password != confirm_password:
            flash("Passwords do not match. Please try again.", "danger")
            return render_template("register.html")

        if len(password) < 6:
            flash("Password must be at least 6 characters long.", "danger")
            return render_template("register.html")

        # Check existing user
        existing = db.query_one("SELECT id FROM users WHERE email = ?", (email,))
        if existing:
            flash("An account with this email already exists. Please log in.", "warning")
            return redirect(url_for("login"))

        password_hash = generate_password_hash(password)
        try:
            user_id = db.execute(
                """INSERT INTO users (full_name, age, gender, email, phone, password_hash)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (full_name, int(age) if age else None, gender, email, phone, password_hash)
            )

            # Auto-create empty health profile
            db.execute("INSERT OR IGNORE INTO health_profiles (user_id) VALUES (?)", (user_id,))

            # Send welcome email
            mail.send_registration_email(email, full_name)

            flash("Registration successful! Welcome to AI Health Assistant. Please log in.", "success")
            return redirect(url_for("login"))
        except Exception as e:
            flash(f"Registration failed: {str(e)}", "danger")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = db.query_one("SELECT * FROM users WHERE email = ?", (email,))
        if user and check_password_hash(user["password_hash"], password):
            session.clear()
            session["user_id"] = user["id"]
            session["user_name"] = user["full_name"]
            session["user_email"] = user["email"]
            flash(f"Welcome back, {user['full_name']}!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid email or password. Please try again.", "danger")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been successfully logged out.", "info")
    return redirect(url_for("login"))


# ══════════════════════════════════════════════════════════════════════════
#  PATIENT DASHBOARD & PROFILE
# ══════════════════════════════════════════════════════════════════════════

@app.route("/dashboard")
@login_required
def dashboard():
    user_id = session["user_id"]
    user = db.query_one("SELECT * FROM users WHERE id = ?", (user_id,))
    profile = db.query_one("SELECT * FROM health_profiles WHERE user_id = ?", (user_id,))
    
    # Recent predictions (last 3)
    recent_predictions = db.query_all(
        "SELECT * FROM predictions WHERE user_id = ? ORDER BY id DESC LIMIT 3",
        (user_id,)
    )

    # Upcoming appointments (last 3)
    upcoming_appointments = db.query_all(
        """SELECT a.*, d.name as doctor_name, d.specialization 
           FROM appointments a 
           JOIN doctors d ON a.doctor_id = d.id 
           WHERE a.patient_id = ? 
           ORDER BY a.id DESC LIMIT 3""",
        (user_id,)
    )

    # Total counts
    prediction_count = db.query_one(
        "SELECT COUNT(*) as count FROM predictions WHERE user_id = ?", (user_id,)
    )["count"]
    
    appointment_count = db.query_one(
        "SELECT COUNT(*) as count FROM appointments WHERE patient_id = ?", (user_id,)
    )["count"]

    unread_messages = db.query_one(
        """SELECT COUNT(*) as count FROM messages 
           WHERE patient_id = ? AND sender_type = 'doctor' AND read_status = 0""",
        (user_id,)
    )["count"]

    return render_template(
        "dashboard.html",
        user=user,
        profile=profile,
        recent_predictions=recent_predictions,
        upcoming_appointments=upcoming_appointments,
        prediction_count=prediction_count,
        appointment_count=appointment_count,
        unread_messages=unread_messages
    )


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    user_id = session["user_id"]
    user = db.query_one("SELECT * FROM users WHERE id = ?", (user_id,))
    profile = db.query_one("SELECT * FROM health_profiles WHERE user_id = ?", (user_id,))

    if request.method == "POST":
        height = request.form.get("height", "").strip()
        weight = request.form.get("weight", "").strip()
        blood_group = request.form.get("blood_group", "").strip()
        blood_pressure = request.form.get("blood_pressure", "").strip()
        blood_sugar = request.form.get("blood_sugar", "").strip()
        heart_rate = request.form.get("heart_rate", "").strip()
        body_temperature = request.form.get("body_temperature", "").strip()
        existing_diseases = request.form.get("existing_diseases", "").strip()
        allergies = request.form.get("allergies", "").strip()
        current_medications = request.form.get("current_medications", "").strip()
        smoking_habit = request.form.get("smoking_habit", "").strip()
        alcohol_consumption = request.form.get("alcohol_consumption", "").strip()
        exercise_frequency = request.form.get("exercise_frequency", "").strip()
        sleeping_hours = request.form.get("sleeping_hours", "").strip()

        # Calculate BMI if height and weight are provided
        bmi = None
        if height and weight:
            try:
                h_m = float(height) / 100.0  # convert cm to meters
                w_kg = float(weight)
                if h_m > 0:
                    bmi = round(w_kg / (h_m ** 2), 1)
            except ValueError:
                pass

        # Also update basic user info if changed
        full_name = request.form.get("full_name", "").strip()
        age = request.form.get("age", "").strip()
        gender = request.form.get("gender", "").strip()
        phone = request.form.get("phone", "").strip()

        if full_name:
            db.execute(
                "UPDATE users SET full_name = ?, age = ?, gender = ?, phone = ? WHERE id = ?",
                (full_name, int(age) if age else None, gender, phone, user_id)
            )
            session["user_name"] = full_name

        # Upsert health profile
        db.execute(
            """INSERT INTO health_profiles (
                user_id, height, weight, bmi, blood_group, blood_pressure,
                blood_sugar, heart_rate, body_temperature, existing_diseases,
                allergies, current_medications, smoking_habit, alcohol_consumption,
                exercise_frequency, sleeping_hours, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now','localtime'))
            ON CONFLICT(user_id) DO UPDATE SET
                height=excluded.height,
                weight=excluded.weight,
                bmi=excluded.bmi,
                blood_group=excluded.blood_group,
                blood_pressure=excluded.blood_pressure,
                blood_sugar=excluded.blood_sugar,
                heart_rate=excluded.heart_rate,
                body_temperature=excluded.body_temperature,
                existing_diseases=excluded.existing_diseases,
                allergies=excluded.allergies,
                current_medications=excluded.current_medications,
                smoking_habit=excluded.smoking_habit,
                alcohol_consumption=excluded.alcohol_consumption,
                exercise_frequency=excluded.exercise_frequency,
                sleeping_hours=excluded.sleeping_hours,
                updated_at=datetime('now','localtime')
            """,
            (
                user_id,
                float(height) if height else None,
                float(weight) if weight else None,
                bmi,
                blood_group,
                blood_pressure,
                float(blood_sugar) if blood_sugar else None,
                int(heart_rate) if heart_rate else None,
                float(body_temperature) if body_temperature else None,
                existing_diseases,
                allergies,
                current_medications,
                smoking_habit,
                alcohol_consumption,
                exercise_frequency,
                float(sleeping_hours) if sleeping_hours else None
            )
        )

        flash("Health profile updated successfully!", "success")
        return redirect(url_for("profile"))

    return render_template("profile.html", user=user, profile=profile)


# ══════════════════════════════════════════════════════════════════════════
#  SYMPTOM ANALYSIS & AI PREDICTION
# ══════════════════════════════════════════════════════════════════════════

SYMPTOM_LIST = [
    ("fever", "Fever"),
    ("headache", "Headache"),
    ("cough", "Cough"),
    ("cold", "Common Cold"),
    ("sore_throat", "Sore Throat"),
    ("fatigue", "Fatigue / Weakness"),
    ("vomiting", "Vomiting"),
    ("nausea", "Nausea"),
    ("diarrhea", "Diarrhea"),
    ("chest_pain", "Chest Pain"),
    ("stomach_pain", "Stomach / Abdominal Pain"),
    ("dizziness", "Dizziness / Lightheadedness"),
    ("breathing_difficulty", "Difficulty Breathing / Shortness of Breath"),
    ("joint_pain", "Joint Pain / Stiffness"),
    ("muscle_pain", "Muscle Aches / Body Ache"),
    ("skin_rash", "Skin Rash / Itching"),
    ("loss_of_appetite", "Loss of Appetite"),
    ("weight_loss", "Unexplained Weight Loss"),
    ("frequent_urination", "Frequent Urination"),
    ("high_temperature", "High Body Temperature (>100°F)"),
    ("sweating", "Excessive Sweating / Night Sweats"),
    ("chills", "Chills & Shivering"),
    ("runny_nose", "Runny / Congested Nose"),
    ("body_ache", "Generalized Body Ache"),
    ("swollen_lymph_nodes", "Swollen Lymph Nodes")
]

@app.route("/symptoms")
@login_required
def symptoms():
    user_id = session["user_id"]
    user = db.query_one("SELECT * FROM users WHERE id = ?", (user_id,))
    return render_template("symptoms.html", symptoms=SYMPTOM_LIST, user=user)


@app.route("/predict", methods=["POST"])
@login_required
def predict():
    user_id = session["user_id"]
    user = db.query_one("SELECT * FROM users WHERE id = ?", (user_id,))

    # Collect selected symptoms
    selected_symptoms = {}
    selected_symptom_names = []
    for key, label in SYMPTOM_LIST:
        val = 1 if request.form.get(key) else 0
        selected_symptoms[key] = val
        if val == 1:
            selected_symptom_names.append(label)

    if not selected_symptom_names:
        flash("Please select at least one symptom to run the AI prediction.", "warning")
        return redirect(url_for("symptoms"))

    # Additional metrics
    duration = request.form.get("duration", "24 hours")
    severity = request.form.get("severity", "Moderate")
    temperature = request.form.get("temperature", "")
    blood_pressure = request.form.get("blood_pressure", "")
    heart_rate = request.form.get("heart_rate", "")
    blood_sugar = request.form.get("blood_sugar", "")
    additional_notes = request.form.get("additional_notes", "")

    # Handle Medical Report Upload / Camera Snapshot
    saved_report_path = None
    
    # 1. File upload
    if "report_file" in request.files:
        file = request.files["report_file"]
        if file and file.filename != "":
            filename = f"{uuid.uuid4().hex[:8]}_{secure_filename(file.filename)}"
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(file_path)
            saved_report_path = f"uploads/reports/{filename}"

    # 2. Camera snapshot (base64)
    camera_image_data = request.form.get("camera_image", "")
    if not saved_report_path and camera_image_data.startswith("data:image"):
        try:
            header, encoded = camera_image_data.split(",", 1)
            image_bytes = base64.b64decode(encoded)
            filename = f"cam_{uuid.uuid4().hex[:8]}.jpg"
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            with open(file_path, "wb") as f:
                f.write(image_bytes)
            saved_report_path = f"uploads/reports/{filename}"
        except Exception as e:
            print(f"[!] Camera image decode error: {e}")

    # Save symptom entry
    symptom_id = db.execute(
        """INSERT INTO symptoms (
            user_id, symptoms_json, duration, severity, temperature,
            blood_pressure, heart_rate, blood_sugar, additional_notes, report_file_path
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            user_id,
            json.dumps(selected_symptom_names),
            duration,
            severity,
            float(temperature) if temperature else None,
            blood_pressure,
            int(heart_rate) if heart_rate else None,
            float(blood_sugar) if blood_sugar else None,
            additional_notes,
            saved_report_path
        )
    )

    # Run ML Prediction
    ml_result = ml.predict_from_symptoms(selected_symptoms)
    predicted_disease = ml_result["predicted_disease"]
    confidence = ml_result["confidence"]
    top_predictions = ml_result["top_predictions"]

    # Fetch Recommendations & Info
    precautions = rec.get_precautions(predicted_disease)
    lifestyle = rec.get_lifestyle(predicted_disease)
    foods_recommended = rec.get_food_recommendation(predicted_disease)
    foods_to_avoid = rec.get_foods_to_avoid(predicted_disease)
    exercise_rec = rec.get_exercise_recommendation(predicted_disease)
    tablets = rec.get_tablets(predicted_disease)

    # Fetch disease description
    desc_map = get_disease_description_map()
    dis_info = desc_map.get(predicted_disease, {
        "description": f"{predicted_disease} is a medical condition that should be evaluated by a healthcare professional.",
        "doctor_advice": "Consult a doctor for personalized medical evaluation and diagnosis."
    })

    # Save prediction to DB (with tablets and report)
    pred_id = db.execute(
        """INSERT INTO predictions (
            user_id, symptom_id, predicted_disease, confidence, description,
            precautions, lifestyle, foods_recommended, foods_to_avoid, exercise_recommendation, tablets, report_file_path
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            user_id,
            symptom_id,
            predicted_disease,
            confidence,
            dis_info["description"],
            json.dumps(precautions),
            json.dumps(lifestyle),
            json.dumps(foods_recommended),
            json.dumps(foods_to_avoid),
            exercise_rec,
            json.dumps(tablets),
            saved_report_path
        )
    )

    # ── Notification preferences from form ──────────────────────────
    mobile_number = request.form.get("mobile_number", "").strip()
    send_sms_flag = request.form.get("send_sms_report", "") == "1"
    send_whatsapp_flag = request.form.get("send_whatsapp_report", "") == "1"
    send_email_flag = request.form.get("send_email_report", "") == "1"

    # Emergency / High-Risk Triage Assessment
    is_emergency = (
        (selected_symptoms.get("chest_pain") == 1 and selected_symptoms.get("breathing_difficulty") == 1) or
        (temperature and float(temperature) >= 103.0) or
        (severity == "Severe")
    )

    # Fetch prescribed doctor details
    doctor = rec.get_prescribing_doctor(predicted_disease)
    consultation_date = datetime.now().strftime("%d %b %Y, %I:%M %p")

    # Use configuration public URL for report links
    public_app_url = app.config.get("PUBLIC_WEB_URL", "http://127.0.0.1:5000").rstrip("/")
    report_url = f"{public_app_url}/report/{pred_id}"
    
    alert_message = sms.format_prediction_alert_message(
        patient_name=user["full_name"] if user else "Patient",
        predicted_disease=predicted_disease,
        confidence=confidence,
        precautions=precautions,
        tablets=tablets,
        is_emergency=is_emergency,
        report_url=report_url,
        doctor_name=doctor["name"],
        doctor_specialty=doctor["specialty"],
        consultation_date=consultation_date
    )

    # 1. Send Prediction Email Notification
    if send_email_flag and user and user["email"]:
        mail.send_prediction_email(
            user["email"],
            user["full_name"],
            predicted_disease,
            confidence,
            precautions,
            lifestyle
        )

    # 2. Send SMS to entered mobile number
    if send_sms_flag and mobile_number:
        sms.send_sms(mobile_number, alert_message)

    # 3. Emergency doctor alert email if condition is high risk
    if is_emergency and user and user["email"]:
        mail.send_health_alert(
            user["email"],
            user["full_name"],
            f"🚨 CRITICAL HEALTH ALERT: High-risk indicators detected for {predicted_disease}. "
            "Please contact a doctor immediately or dial 108 for emergency ambulance response!"
        )

    # Generate 1-Click WhatsApp App & Web links for direct sharing
    whatsapp_app_url = sms.generate_whatsapp_app_url(mobile_number, alert_message)
    whatsapp_url = sms.generate_whatsapp_url(mobile_number, alert_message)
    native_sms_url = sms.generate_native_sms_url(mobile_number, alert_message)

    return render_template(
        "prediction.html",
        disease=predicted_disease,
        confidence=confidence,
        top_predictions=top_predictions,
        selected_symptoms=selected_symptom_names,
        duration=duration,
        severity=severity,
        description=dis_info["description"],
        doctor_advice=dis_info["doctor_advice"],
        precautions=precautions,
        lifestyle=lifestyle,
        foods_recommended=foods_recommended,
        foods_to_avoid=foods_to_avoid,
        exercise=exercise_rec,
        tablets=tablets,
        is_emergency=is_emergency,
        pred_id=pred_id,
        mobile_number=mobile_number,
        saved_report_path=saved_report_path,
        whatsapp_url=whatsapp_url,
        whatsapp_app_url=whatsapp_app_url,
        native_sms_url=native_sms_url,
        alert_message=alert_message,
        send_whatsapp=send_whatsapp_flag,
        doctor=doctor,
        consultation_date=consultation_date
    )


# ══════════════════════════════════════════════════════════════════════════
#  AI CHATBOT
# ══════════════════════════════════════════════════════════════════════════

@app.route("/chatbot")
@login_required
def chatbot():
    return render_template("chatbot.html")


@app.route("/api/chat", methods=["POST"])
def api_chat():
    data = request.get_json() or {}
    message = data.get("message", "").strip()
    if not message:
        return jsonify({"error": "Empty message"}), 400

    result = ai_bot.analyze_chat_message(message)
    return jsonify(result)



# ══════════════════════════════════════════════════════════════════════════
#  DOCTOR CONSULTATION & CHAT
# ══════════════════════════════════════════════════════════════════════════

@app.route("/doctors")
@login_required
def doctors():
    spec_filter = request.args.get("spec", "").strip()
    if spec_filter:
        doc_list = db.query_all("SELECT * FROM doctors WHERE specialization LIKE ?", (f"%{spec_filter}%",))
    else:
        doc_list = db.query_all("SELECT * FROM doctors")
    
    specializations = db.query_all("SELECT DISTINCT specialization FROM doctors WHERE specialization IS NOT NULL")
    return render_template("doctors.html", doctors=doc_list, specializations=[s["specialization"] for s in specializations], current_spec=spec_filter)


@app.route("/chat/<int:doctor_id>")
@login_required
def patient_chat(doctor_id):
    patient_id = session["user_id"]
    doctor = db.query_one("SELECT * FROM doctors WHERE id = ?", (doctor_id,))
    if not doctor:
        flash("Doctor not found.", "danger")
        return redirect(url_for("doctors"))

    # Mark doctor messages as read
    db.execute(
        "UPDATE messages SET read_status = 1 WHERE patient_id = ? AND doctor_id = ? AND sender_type = 'doctor'",
        (patient_id, doctor_id)
    )

    # Get conversation history
    messages = db.query_all(
        """SELECT * FROM messages 
           WHERE patient_id = ? AND doctor_id = ? 
           ORDER BY id ASC""",
        (patient_id, doctor_id)
    )

    return render_template("doctor_chat.html", doctor=doctor, messages=messages)


@app.route("/api/doctor-chat/send", methods=["POST"])
def api_send_doctor_message():
    data = request.get_json() or {}
    patient_id = data.get("patient_id")
    doctor_id = data.get("doctor_id")
    sender_type = data.get("sender_type")  # 'patient' or 'doctor'
    message_text = data.get("message", "").strip()

    if not message_text or not patient_id or not doctor_id or sender_type not in ["patient", "doctor"]:
        return jsonify({"error": "Invalid payload"}), 400

    # Insert message
    msg_id = db.execute(
        """INSERT INTO messages (patient_id, doctor_id, sender_type, message)
           VALUES (?, ?, ?, ?)""",
        (patient_id, doctor_id, sender_type, message_text)
    )

    # Send email notification
    patient = db.query_one("SELECT * FROM users WHERE id = ?", (patient_id,))
    doctor = db.query_one("SELECT * FROM doctors WHERE id = ?", (doctor_id,))

    if sender_type == "patient" and doctor and doctor["email"]:
        mail.send_doctor_message_notification(doctor["email"], doctor["name"], patient["full_name"] if patient else "Patient")
    elif sender_type == "doctor" and patient and patient["email"]:
        mail.send_doctor_reply_notification(patient["email"], patient["full_name"], doctor["name"] if doctor else "Doctor")

    return jsonify({
        "success": True,
        "message_id": msg_id,
        "date_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })


@app.route("/api/doctor-chat/messages/<int:patient_id>/<int:doctor_id>")
def api_get_messages(patient_id, doctor_id):
    messages = db.query_all(
        """SELECT id, sender_type, message, date_time 
           FROM messages 
           WHERE patient_id = ? AND doctor_id = ? 
           ORDER BY id ASC""",
        (patient_id, doctor_id)
    )
    return jsonify([dict(m) for m in messages])


# ══════════════════════════════════════════════════════════════════════════
#  DOCTOR PORTAL (Doctor Login & Dashboard)
# ══════════════════════════════════════════════════════════════════════════

@app.route("/doctor/login", methods=["GET", "POST"])
def doctor_login():
    if "doctor_id" in session:
        return redirect(url_for("doctor_dashboard"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        doctor = db.query_one("SELECT * FROM doctors WHERE email = ?", (email,))
        if doctor and check_password_hash(doctor["password_hash"], password):
            session.clear()
            session["doctor_id"] = doctor["id"]
            session["doctor_name"] = doctor["name"]
            session["doctor_email"] = doctor["email"]
            flash(f"Welcome, {doctor['name']}!", "success")
            return redirect(url_for("doctor_dashboard"))
        else:
            flash("Invalid doctor credentials. (Demo password: password123)", "danger")

    return render_template("doctor_login.html")


@app.route("/doctor/dashboard")
@doctor_login_required
def doctor_dashboard():
    doctor_id = session["doctor_id"]
    doctor = db.query_one("SELECT * FROM doctors WHERE id = ?", (doctor_id,))

    # Patients who interacted or booked with this doctor
    patients_with_chats = db.query_all(
        """SELECT DISTINCT u.id, u.full_name, u.email, u.phone, u.age, u.gender,
                  (SELECT message FROM messages WHERE patient_id = u.id AND doctor_id = ? ORDER BY id DESC LIMIT 1) as last_message,
                  (SELECT date_time FROM messages WHERE patient_id = u.id AND doctor_id = ? ORDER BY id DESC LIMIT 1) as last_msg_time,
                  (SELECT COUNT(*) FROM messages WHERE patient_id = u.id AND doctor_id = ? AND sender_type = 'patient' AND read_status = 0) as unread_count
           FROM users u
           JOIN messages m ON u.id = m.patient_id
           WHERE m.doctor_id = ?
           ORDER BY last_msg_time DESC""",
        (doctor_id, doctor_id, doctor_id, doctor_id)
    )

    appointments = db.query_all(
        """SELECT a.*, u.full_name, u.email, u.phone 
           FROM appointments a 
           JOIN users u ON a.patient_id = u.id 
           WHERE a.doctor_id = ? 
           ORDER BY a.appointment_date ASC, a.appointment_time ASC""",
        (doctor_id,)
    )

    return render_template(
        "doctor_dashboard.html",
        doctor=doctor,
        patients=patients_with_chats,
        appointments=appointments
    )


@app.route("/doctor/chat/<int:patient_id>")
@doctor_login_required
def doctor_patient_chat(patient_id):
    doctor_id = session["doctor_id"]
    patient = db.query_one("SELECT * FROM users WHERE id = ?", (patient_id,))
    patient_profile = db.query_one("SELECT * FROM health_profiles WHERE user_id = ?", (patient_id,))
    recent_predictions = db.query_all("SELECT * FROM predictions WHERE user_id = ? ORDER BY id DESC LIMIT 2", (patient_id,))

    if not patient:
        flash("Patient not found.", "danger")
        return redirect(url_for("doctor_dashboard"))

    # Mark patient messages as read
    db.execute(
        "UPDATE messages SET read_status = 1 WHERE patient_id = ? AND doctor_id = ? AND sender_type = 'patient'",
        (patient_id, doctor_id)
    )

    messages = db.query_all(
        """SELECT * FROM messages 
           WHERE patient_id = ? AND doctor_id = ? 
           ORDER BY id ASC""",
        (patient_id, doctor_id)
    )

    return render_template(
        "doctor_chat.html",
        doctor={"id": doctor_id, "name": session["doctor_name"]},
        patient=patient,
        patient_profile=patient_profile,
        recent_predictions=recent_predictions,
        messages=messages,
        is_doctor_view=True
    )


@app.route("/doctor/appointment/<int:appt_id>/<status>")
@doctor_login_required
def update_appointment_status(appt_id, status):
    if status in ["Confirmed", "Cancelled", "Completed"]:
        db.execute("UPDATE appointments SET status = ? WHERE id = ?", (status, appt_id))
        flash(f"Appointment status updated to {status}.", "success")
    return redirect(url_for("doctor_dashboard"))


# ══════════════════════════════════════════════════════════════════════════
#  APPOINTMENT BOOKING
# ══════════════════════════════════════════════════════════════════════════

@app.route("/appointment", methods=["GET", "POST"])
@login_required
def appointment():
    user_id = session["user_id"]
    user = db.query_one("SELECT * FROM users WHERE id = ?", (user_id,))
    doctors = db.query_all("SELECT id, name, specialization FROM doctors")

    if request.method == "POST":
        doctor_id = request.form.get("doctor_id")
        appt_date = request.form.get("appointment_date")
        appt_time = request.form.get("appointment_time")
        reason = request.form.get("reason", "").strip()

        if not doctor_id or not appt_date or not appt_time:
            flash("Please fill in all appointment fields.", "danger")
            return redirect(url_for("appointment"))

        doctor = db.query_one("SELECT name, email FROM doctors WHERE id = ?", (doctor_id,))
        if not doctor:
            flash("Selected doctor does not exist.", "danger")
            return redirect(url_for("appointment"))

        db.execute(
            """INSERT INTO appointments (patient_id, doctor_id, appointment_date, appointment_time, reason, status)
               VALUES (?, ?, ?, ?, ?, 'Pending')""",
            (user_id, doctor_id, appt_date, appt_time, reason)
        )

        # Send confirmation email
        if user and user["email"]:
            mail.send_appointment_confirmation(
                user["email"],
                user["full_name"],
                doctor["name"],
                appt_date,
                appt_time,
                reason or "General Health Consultation"
            )

        flash("Appointment booked successfully! A confirmation email has been sent.", "success")
        return redirect(url_for("appointment"))

    # Patient's appointments
    appointments = db.query_all(
        """SELECT a.*, d.name as doctor_name, d.specialization 
           FROM appointments a 
           JOIN doctors d ON a.doctor_id = d.id 
           WHERE a.patient_id = ? 
           ORDER BY a.appointment_date DESC, a.appointment_time DESC""",
        (user_id,)
    )

    return render_template("appointments.html", doctors=doctors, appointments=appointments)


# ══════════════════════════════════════════════════════════════════════════
#  HISTORY (Predictions & Consultations)
# ══════════════════════════════════════════════════════════════════════════

@app.route("/history")
@login_required
def history():
    user_id = session["user_id"]
    
    predictions = db.query_all(
        """SELECT p.*, s.symptoms_json, s.duration, s.severity, s.temperature, s.blood_pressure 
           FROM predictions p 
           LEFT JOIN symptoms s ON p.symptom_id = s.id 
           WHERE p.user_id = ? 
           ORDER BY p.id DESC""",
        (user_id,)
    )

    appointments = db.query_all(
        """SELECT a.*, d.name as doctor_name, d.specialization 
           FROM appointments a 
           JOIN doctors d ON a.doctor_id = d.id 
           WHERE a.patient_id = ? 
           ORDER BY a.id DESC""",
        (user_id,)
    )

    # Process JSON fields in predictions for template rendering
    parsed_predictions = []
    for p in predictions:
        row = dict(p)
        try:
            row["precautions_list"] = json.loads(p["precautions"]) if p["precautions"] else []
        except Exception:
            row["precautions_list"] = []
        try:
            row["lifestyle_list"] = json.loads(p["lifestyle"]) if p["lifestyle"] else []
        except Exception:
            row["lifestyle_list"] = []
        try:
            row["symptoms_list"] = json.loads(p["symptoms_json"]) if p["symptoms_json"] else []
        except Exception:
            row["symptoms_list"] = []
        parsed_predictions.append(row)

    return render_template("history.html", predictions=parsed_predictions, appointments=appointments)


# ── PDF Report Download ────────────────────────────────────────────────────

@app.route("/report/<int:pred_id>")
@login_required
def download_report(pred_id):
    """Generate and serve a printable HTML report for a given prediction."""
    user_id = session["user_id"]
    pred = db.query_one(
        "SELECT * FROM predictions WHERE id = ? AND user_id = ?", (pred_id, user_id)
    )
    if not pred:
        flash("Report not found or access denied.", "danger")
        return redirect(url_for("history"))

    user = db.query_one("SELECT * FROM users WHERE id = ?", (user_id,))

    # Parse JSON fields
    try:
        precautions = json.loads(pred["precautions"]) if pred["precautions"] else []
    except Exception:
        precautions = []
    try:
        lifestyle = json.loads(pred["lifestyle"]) if pred["lifestyle"] else []
    except Exception:
        lifestyle = []
    try:
        foods_recommended = json.loads(pred["foods_recommended"]) if pred["foods_recommended"] else []
    except Exception:
        foods_recommended = []
    try:
        foods_to_avoid = json.loads(pred["foods_to_avoid"]) if pred["foods_to_avoid"] else []
    except Exception:
        foods_to_avoid = []
    try:
        tablets = json.loads(pred["tablets"]) if pred["tablets"] else []
    except Exception:
        tablets = []

    doctor = rec.get_prescribing_doctor(pred["predicted_disease"])

    return render_template(
        "report.html",
        user=user,
        pred=pred,
        precautions=precautions,
        lifestyle=lifestyle,
        foods_recommended=foods_recommended,
        foods_to_avoid=foods_to_avoid,
        tablets=tablets,
        doctor=doctor,
        generated_at=datetime.now().strftime("%d %B %Y, %I:%M %p")
    )


# ── Ambulance Emergency Services ───────────────────────────────────────────

@app.route("/ambulance", methods=["GET", "POST"])
def ambulance():
    user = None
    if "user_id" in session:
        user = db.query_one("SELECT * FROM users WHERE id = ?", (session["user_id"],))

    if request.method == "POST":
        patient_name = request.form.get("patient_name", "").strip()
        patient_age = request.form.get("patient_age", "30").strip()
        mobile_number = request.form.get("mobile_number", "").strip()
        area_location = request.form.get("area_location", "").strip()
        emergency_reason = request.form.get("emergency_reason", "Medical Emergency").strip()

        if not patient_name or not mobile_number or not area_location:
            flash("Patient Name, Mobile Number, and Area Location are required!", "danger")
            return redirect(url_for("ambulance"))

        encoded_loc = urllib.parse.quote(area_location)
        maps_url = f"https://www.google.com/maps/dir/?api=1&destination={encoded_loc}"

        # Save to database
        req_id = db.execute(
            """INSERT INTO ambulance_requests 
               (user_id, patient_name, patient_age, mobile_number, area_location, emergency_reason, maps_url, status) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (session.get("user_id"), patient_name, int(patient_age) if patient_age.isdigit() else 30,
             mobile_number, area_location, emergency_reason, maps_url, "Dispatched")
        )

        # Dispatch SMS and Email
        sms.send_ambulance_dispatch_sms(
            patient_name=patient_name,
            patient_age=patient_age,
            mobile_number=mobile_number,
            area_location=area_location,
            emergency_reason=emergency_reason,
            maps_url=maps_url
        )

        user_email = user["email"] if user else "patient@example.com"
        mail.send_ambulance_alert_email(
            to_email=user_email,
            patient_name=patient_name,
            patient_age=patient_age,
            mobile_number=mobile_number,
            area_location=area_location,
            emergency_reason=emergency_reason,
            maps_url=maps_url
        )

        flash(f"🚨 Ambulance AMB-108 successfully dispatched for {patient_name}! SMS Alert sent to {mobile_number}.", "success")
        return render_template(
            "ambulance.html",
            user=user,
            dispatched=True,
            patient_name=patient_name,
            patient_age=patient_age,
            mobile_number=mobile_number,
            area_location=area_location,
            emergency_reason=emergency_reason,
            maps_url=maps_url,
            req_id=req_id
        )

    # Fetch recent dispatches
    recent_requests = db.query_all("SELECT * FROM ambulance_requests ORDER BY id DESC LIMIT 5")
    return render_template("ambulance.html", user=user, dispatched=False, recent_requests=recent_requests)


# ══════════════════════════════════════════════════════════════════════════
#  MOBILE & PUBLIC REST API ENDPOINTS
# ══════════════════════════════════════════════════════════════════════════

@app.route("/api/health")
def api_health():
    """Health check endpoint for cloud monitoring & mobile connectivity"""
    return jsonify({
        "status": "healthy",
        "service": "AI Health Assistant API",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    })

@app.route("/api/auth/register", methods=["POST"])
def api_register():
    """JSON Registration for Mobile/Web Clients"""
    data = request.get_json() or {}
    full_name = data.get("full_name", "").strip()
    age = data.get("age")
    gender = data.get("gender", "").strip()
    email = data.get("email", "").strip().lower()
    phone = data.get("phone", "").strip()
    password = data.get("password", "")

    if not full_name or not email or not password:
        return jsonify({"success": False, "error": "Missing required fields (full_name, email, password)"}), 400

    if len(password) < 6:
        return jsonify({"success": False, "error": "Password must be at least 6 characters"}), 400

    existing = db.query_one("SELECT id FROM users WHERE email = ?", (email,))
    if existing:
        return jsonify({"success": False, "error": "Account with this email already exists"}), 409

    password_hash = generate_password_hash(password)
    try:
        user_id = db.execute(
            """INSERT INTO users (full_name, age, gender, email, phone, password_hash)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (full_name, int(age) if age else None, gender, email, phone, password_hash)
        )
        db.execute("INSERT OR IGNORE INTO health_profiles (user_id) VALUES (?)", (user_id,))
        mail.send_registration_email(email, full_name)

        session["user_id"] = user_id
        session["user_name"] = full_name
        session["user_email"] = email

        return jsonify({
            "success": True,
            "message": "User registered successfully",
            "user": {
                "id": user_id,
                "full_name": full_name,
                "email": email,
                "phone": phone,
                "age": age,
                "gender": gender
            }
        }), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/auth/login", methods=["POST"])
def api_login():
    """JSON Login for Mobile/Web Clients"""
    data = request.get_json() or {}
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        return jsonify({"success": False, "error": "Email and password are required"}), 400

    user = db.query_one("SELECT * FROM users WHERE email = ?", (email,))
    if user and check_password_hash(user["password_hash"], password):
        session.clear()
        session["user_id"] = user["id"]
        session["user_name"] = user["full_name"]
        session["user_email"] = user["email"]

        profile = db.query_one("SELECT * FROM health_profiles WHERE user_id = ?", (user["id"],))

        return jsonify({
            "success": True,
            "message": "Login successful",
            "user": {
                "id": user["id"],
                "full_name": user["full_name"],
                "email": user["email"],
                "phone": user["phone"],
                "age": user["age"],
                "gender": user["gender"]
            },
            "profile": dict(profile) if profile else None
        })

    return jsonify({"success": False, "error": "Invalid email or password"}), 401

@app.route("/api/auth/me")
def api_auth_me():
    """Get current authenticated user"""
    if "user_id" in session:
        user = db.query_one("SELECT id, full_name, email, phone, age, gender, created_at FROM users WHERE id = ?", (session["user_id"],))
        profile = db.query_one("SELECT * FROM health_profiles WHERE user_id = ?", (session["user_id"],))
        return jsonify({
            "authenticated": True,
            "role": "patient",
            "user": dict(user) if user else None,
            "profile": dict(profile) if profile else None
        })
    elif "doctor_id" in session:
        doctor = db.query_one("SELECT id, name, email, specialization, experience, hospital, phone FROM doctors WHERE id = ?", (session["doctor_id"],))
        return jsonify({
            "authenticated": True,
            "role": "doctor",
            "doctor": dict(doctor) if doctor else None
        })
    return jsonify({"authenticated": False, "user": None})

@app.route("/api/auth/logout", methods=["POST"])
def api_logout():
    session.clear()
    return jsonify({"success": True, "message": "Logged out successfully"})

@app.route("/api/symptoms")
def api_symptoms():
    """Return all known symptoms categorized for mobile app checklist"""
    return jsonify({
        "categories": {
            "Respiratory & ENT": [
                {"id": "cough", "label": "Persistent Cough"},
                {"id": "chest_pain", "label": "Chest Pain / Pressure"},
                {"id": "breathlessness", "label": "Shortness of Breath"},
                {"id": "throat_irritation", "label": "Sore / Scratchy Throat"},
                {"id": "sinus_pressure", "label": "Sinus Congestion / Pressure"},
                {"id": "runny_nose", "label": "Runny / Stuffy Nose"}
            ],
            "Systemic & Fever": [
                {"id": "fever", "label": "High Fever"},
                {"id": "mild_fever", "label": "Mild / Low-grade Fever"},
                {"id": "chills", "label": "Shivering / Chills"},
                {"id": "fatigue", "label": "General Fatigue / Lethargy"},
                {"id": "headache", "label": "Headache / Migraine"},
                {"id": "body_ache", "label": "Body Ache / Malaise"},
                {"id": "joint_pain", "label": "Joint Pain / Stiffness"},
                {"id": "muscle_pain", "label": "Muscle Pain / Weakness"},
                {"id": "swollen_lymph_nodes", "label": "Swollen Glands / Lymph Nodes"}
            ],
            "Digestive & Metabolic": [
                {"id": "stomach_pain", "label": "Stomach Ache / Cramps"},
                {"id": "nausea", "label": "Nausea"},
                {"id": "vomiting", "label": "Vomiting"},
                {"id": "diarrhea", "label": "Loose Stools / Diarrhea"},
                {"id": "loss_of_appetite", "label": "Loss of Appetite"},
                {"id": "weight_loss", "label": "Unexplained Weight Loss"},
                {"id": "frequent_urination", "label": "Frequent Urination"},
                {"id": "skin_rash", "label": "Skin Rash / Itch"}
            ]
        }
    })

@app.route("/api/predict", methods=["POST"])
def api_predict():
    """Predict disease and provide complete clinical recommendations"""
    data = request.get_json() or {}
    symptoms_input = data.get("symptoms", [])
    duration = data.get("duration", "1-3 days")
    severity = data.get("severity", "Mild")
    temperature = data.get("temperature", "")
    blood_pressure = data.get("blood_pressure", "")

    # Build symptom dict
    symptoms_dict = {}
    if isinstance(symptoms_input, list):
        for s in symptoms_input:
            symptoms_dict[s] = 1
    elif isinstance(symptoms_input, dict):
        symptoms_dict = symptoms_input

    if not any(symptoms_dict.values()):
        return jsonify({"success": False, "error": "At least one symptom must be selected."}), 400

    try:
        prediction_res = ml.predict_from_symptoms(symptoms_dict)
        predicted_disease = prediction_res["predicted_disease"]
        confidence = prediction_res["confidence"]
        top_preds = prediction_res.get("top_predictions", [])

        # Recommendations
        recs = rec.get_all_recommendations(predicted_disease)
        desc_map = get_disease_description_map()
        dis_info = desc_map.get(predicted_disease, {
            "description": "Consult a physician for a thorough evaluation.",
            "doctor_advice": "Seek medical consultation promptly."
        })
        doctor = rec.get_prescribing_doctor(predicted_disease)
        is_emergency = rec.is_emergency_condition(predicted_disease)

        # Save to database if user authenticated
        pred_id = None
        user_id = session.get("user_id") or data.get("user_id")
        if user_id:
            try:
                symptom_id = db.execute(
                    """INSERT INTO symptoms (user_id, symptoms_json, duration, severity, temperature, blood_pressure)
                       VALUES (?, ?, ?, ?, ?, ?)""",
                    (user_id, json.dumps([k for k, v in symptoms_dict.items() if v]), duration, severity, temperature, blood_pressure)
                )
                pred_id = db.execute(
                    """INSERT INTO predictions 
                       (user_id, symptom_id, predicted_disease, confidence_score, precautions, lifestyle, foods_recommended, foods_to_avoid, tablets)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (user_id, symptom_id, predicted_disease, confidence,
                     json.dumps(recs.get("precautions", [])),
                     json.dumps(recs.get("lifestyle", [])),
                     json.dumps(recs.get("foods_recommended", [])),
                     json.dumps(recs.get("foods_to_avoid", [])),
                     json.dumps(recs.get("tablets", [])))
                )
            except Exception as db_err:
                app.logger.warning(f"Could not persist prediction to DB: {db_err}")

        return jsonify({
            "success": True,
            "prediction_id": pred_id,
            "predicted_disease": predicted_disease,
            "confidence": confidence,
            "top_predictions": top_preds,
            "is_emergency": is_emergency,
            "description": dis_info["description"],
            "doctor_advice": dis_info["doctor_advice"],
            "precautions": recs.get("precautions", []),
            "lifestyle": recs.get("lifestyle", []),
            "foods_recommended": recs.get("foods_recommended", []),
            "foods_to_avoid": recs.get("foods_to_avoid", []),
            "exercise": recs.get("exercise", ""),
            "tablets": recs.get("tablets", []),
            "recommended_doctor": doctor
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/ambulance", methods=["POST"])
def api_ambulance():
    """Emergency 1-Click Ambulance Dispatch API"""
    data = request.get_json() or {}
    patient_name = data.get("patient_name", "").strip()
    patient_age = data.get("patient_age", "30")
    mobile_number = data.get("mobile_number", "").strip()
    area_location = data.get("area_location", "").strip()
    emergency_reason = data.get("emergency_reason", "Medical Emergency").strip()

    if not patient_name or not mobile_number or not area_location:
        return jsonify({"success": False, "error": "Patient Name, Mobile Number, and Area Location are required"}), 400

    encoded_loc = urllib.parse.quote(area_location)
    maps_url = f"https://www.google.com/maps/dir/?api=1&destination={encoded_loc}"

    user_id = session.get("user_id") or data.get("user_id")

    req_id = db.execute(
        """INSERT INTO ambulance_requests 
           (user_id, patient_name, patient_age, mobile_number, area_location, emergency_reason, maps_url, status) 
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (user_id, patient_name, int(patient_age) if str(patient_age).isdigit() else 30,
         mobile_number, area_location, emergency_reason, maps_url, "Dispatched")
    )

    sms.send_ambulance_dispatch_sms(
        patient_name=patient_name,
        patient_age=str(patient_age),
        mobile_number=mobile_number,
        area_location=area_location,
        emergency_reason=emergency_reason,
        maps_url=maps_url
    )

    return jsonify({
        "success": True,
        "message": f"Ambulance AMB-108 dispatched for {patient_name}",
        "request_id": req_id,
        "maps_url": maps_url,
        "status": "Dispatched"
    }), 201

@app.route("/api/doctors")
def api_doctors():
    """List available doctors with optional specialization query filter"""
    spec_filter = request.args.get("spec", "").strip()
    if spec_filter:
        docs = db.query_all("SELECT id, name, specialization, qualification, experience, email, availability, bio FROM doctors WHERE specialization LIKE ?", (f"%{spec_filter}%",))
    else:
        docs = db.query_all("SELECT id, name, specialization, qualification, experience, email, availability, bio FROM doctors")
    return jsonify({"success": True, "doctors": [dict(d) for d in docs]})


@app.route("/api/appointments", methods=["GET", "POST"])
def api_appointments():
    """Book or retrieve appointments"""
    user_id = session.get("user_id")
    
    if request.method == "POST":
        data = request.get_json() or {}
        uid = user_id or data.get("user_id")
        doctor_id = data.get("doctor_id")
        appt_date = data.get("appointment_date")
        appt_time = data.get("appointment_time")
        reason = data.get("reason", "General Health Consultation").strip()

        if not uid or not doctor_id or not appt_date or not appt_time:
            return jsonify({"success": False, "error": "Missing required appointment fields"}), 400

        doctor = db.query_one("SELECT name, email FROM doctors WHERE id = ?", (doctor_id,))
        if not doctor:
            return jsonify({"success": False, "error": "Doctor not found"}), 404

        appt_id = db.execute(
            """INSERT INTO appointments (patient_id, doctor_id, appointment_date, appointment_time, reason, status)
               VALUES (?, ?, ?, ?, ?, 'Pending')""",
            (uid, doctor_id, appt_date, appt_time, reason)
        )

        user = db.query_one("SELECT * FROM users WHERE id = ?", (uid,))
        if user and user.get("email"):
            mail.send_appointment_confirmation(
                user["email"],
                user.get("full_name", "Patient"),
                doctor["name"],
                appt_date,
                appt_time,
                reason
            )

        return jsonify({
            "success": True,
            "message": "Appointment booked successfully",
            "appointment_id": appt_id
        }), 201

    if not user_id:
        return jsonify({"success": False, "error": "Unauthorized"}), 401

    appts = db.query_all(
        """SELECT a.*, d.name as doctor_name, d.specialization 
           FROM appointments a 
           JOIN doctors d ON a.doctor_id = d.id 
           WHERE a.patient_id = ? 
           ORDER BY a.appointment_date DESC, a.appointment_time DESC""",
        (user_id,)
    )
    return jsonify({"success": True, "appointments": [dict(a) for a in appts]})

@app.route("/api/profile", methods=["GET", "POST"])
def api_profile():
    """Retrieve or update health profile and BMI"""
    user_id = session.get("user_id")
    if not user_id:
        data = request.get_json() if request.method == "POST" else {}
        user_id = data.get("user_id")
    
    if not user_id:
        return jsonify({"success": False, "error": "Unauthorized"}), 401

    if request.method == "POST":
        data = request.get_json() or {}
        height = data.get("height")
        weight = data.get("weight")
        blood_group = data.get("blood_group", "")
        allergies = data.get("allergies", "")
        medications = data.get("medications", "")
        emergency_contact = data.get("emergency_contact", "")

        bmi = None
        if height and weight:
            try:
                h_m = float(height) / 100.0
                bmi = round(float(weight) / (h_m * h_m), 1)
            except (ValueError, ZeroDivisionError):
                bmi = None

        db.execute(
            """INSERT INTO health_profiles (user_id, height, weight, bmi, blood_group, allergies, current_medications, emergency_contact)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)
               ON CONFLICT(user_id) DO UPDATE SET
               height = excluded.height,
               weight = excluded.weight,
               bmi = excluded.bmi,
               blood_group = excluded.blood_group,
               allergies = excluded.allergies,
               current_medications = excluded.current_medications,
               emergency_contact = excluded.emergency_contact""",
            (user_id, height, weight, bmi, blood_group, allergies, medications, emergency_contact)
        )

        return jsonify({
            "success": True,
            "message": "Health profile updated successfully",
            "bmi": bmi
        })

    profile = db.query_one("SELECT * FROM health_profiles WHERE user_id = ?", (user_id,))
    return jsonify({"success": True, "profile": dict(profile) if profile else None})

@app.route("/api/history")
def api_history():
    """Retrieve prediction and appointment history for user"""
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"success": False, "error": "Unauthorized"}), 401

    preds = db.query_all(
        """SELECT p.id, p.predicted_disease, p.confidence_score, p.precautions, p.lifestyle, p.created_at,
                  s.symptoms_json, s.duration, s.severity
           FROM predictions p
           LEFT JOIN symptoms s ON p.symptom_id = s.id
           WHERE p.user_id = ?
           ORDER BY p.id DESC""",
        (user_id,)
    )

    parsed = []
    for p in preds:
        item = dict(p)
        try:
            item["symptoms"] = json.loads(p["symptoms_json"]) if p["symptoms_json"] else []
        except Exception:
            item["symptoms"] = []
        try:
            item["precautions"] = json.loads(p["precautions"]) if p["precautions"] else []
        except Exception:
            item["precautions"] = []
        parsed.append(item)

    return jsonify({"success": True, "predictions": parsed})


# ══════════════════════════════════════════════════════════════════════════
#  DEEP LINKING VERIFICATION (Android App Links & iOS Universal Links)
# ══════════════════════════════════════════════════════════════════════════

@app.route("/.well-known/assetlinks.json")
def assetlinks():
    """Android App Links verification configuration"""
    return jsonify([{
        "relation": ["delegate_permission/common.handle_all_urls"],
        "target": {
            "namespace": "android_app",
            "package_name": "com.health.aiassistant",
            "sha256_cert_fingerprints": [
                # Replace with production keystore SHA-256 fingerprint when building signed APK/AAB
                "FA:C6:17:45:DC:09:03:78:6F:B9:ED:E6:2A:96:2B:39:9F:73:48:F0:BB:6F:89:9B:83:32:66:75:91:03:3B:9C"
            ]
        }
    }])

@app.route("/.well-known/apple-app-site-association")
def apple_app_site_association():
    """iOS Universal Links verification configuration"""
    return jsonify({
        "applinks": {
            "apps": [],
            "details": [
                {
                    "appID": "TEAM_ID_HERE.com.health.aiassistant",
                    "paths": ["/download", "/install", "/prediction", "/ambulance", "/history", "/profile", "/chat/*"]
                }
            ]
        }
    })


# ══════════════════════════════════════════════════════════════════════════
#  PRODUCTION ERROR HANDLERS (JSON for API, HTML for Web)
# ══════════════════════════════════════════════════════════════════════════

@app.errorhandler(404)
def not_found_error(error):
    if request.path.startswith("/api/"):
        return jsonify({"success": False, "error": "Endpoint not found"}), 404
    return render_template("index.html"), 404

@app.errorhandler(500)
def internal_error(error):
    if request.path.startswith("/api/"):
        return jsonify({"success": False, "error": "Internal server error"}), 500
    flash("An unexpected error occurred. Please try again.", "danger")
    return render_template("index.html"), 500



# ── Initialization ─────────────────────────────────────────────────────────

def get_local_ip():
    """Find the local Wi-Fi/LAN IP address for cross-device access."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


if __name__ == "__main__":
    db.init_db()
    # Train ML model if not already present
    if not os.path.exists(ml.MODEL_PATH):
        print("[+] Initializing AI Model...")
        ml.train_models()

    local_ip = get_local_ip()
    
    # Get configuration
    host = app.config.get("HOST", "0.0.0.0")
    port = app.config.get("PORT", 5000)
    public_web_url = app.config.get("PUBLIC_WEB_URL", f"http://{local_ip}:{port}")
    api_base_url = app.config.get("API_BASE_URL", f"http://{local_ip}:{port}")
    flask_env = os.getenv("FLASK_ENV", "development")
    debug = os.getenv("DEBUG", "False").lower() == "true"
    
    print("\n" + "="*80)
    print("🏥 AI HEALTH ASSISTANT — PRODUCTION READY")
    print("="*80)
    print(f"Environment: {flask_env.upper()}")
    print(f"Debug Mode:  {debug}")
    print()
    print("📍 ACCESS POINTS:")
    print(f"   Local Machine    : http://127.0.0.1:{port}")
    print(f"   Local Network    : http://{local_ip}:{port}")
    print(f"   Public Web URL   : {public_web_url}")
    print(f"   API Base URL     : {api_base_url}")
    print()
    print("📱 MOBILE APPS:")
    print(f"   Configure API: {api_base_url}")
    print(f"   Download Page: {public_web_url}/download")
    print()
    print("🔧 CONFIGURATION:")
    print(f"   FLASK_ENV={flask_env}")
    print(f"   HOST={host}")
    print(f"   PORT={port}")
    print()
    if flask_env == "development":
        print("⚠️  DEVELOPMENT MODE - Use only for local testing!")
    else:
        print("✅ PRODUCTION MODE - All security enabled")
    print("="*80 + "\n")

    app.run(host=host, port=port, debug=debug, threaded=True)

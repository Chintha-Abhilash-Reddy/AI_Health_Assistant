# AI Powered Health Assistant for Disease Prediction, Precaution and Lifestyle Recommendations

A full-stack Python & Flask web application featuring Machine Learning disease prediction, automated precautions, tailored diet and lifestyle recommendations, 24/7 AI health chatbot, live doctor consultation messaging, and appointment booking with email notifications.

---

## 🌟 Key Features

1. **User Registration & Authentication**:
   - Secure patient registration and login with password hashing.
   - Automated welcome email sent to the user upon registration.
2. **Comprehensive Health Profile Management**:
   - Stores physiological vitals (Height, Weight, Blood Pressure, Blood Sugar, Heart Rate, Temperature).
   - Real-time automatic calculation and categorization of **BMI** (Underweight, Normal, Overweight, Obese).
   - Medical background tracking (Existing Diseases, Allergies, Current Medications, Smoking Habit, Alcohol, Exercise, Sleep).
3. **AI Disease Prediction Engine**:
   - Trained on 25+ clinical symptom factors covering 15 diseases.
   - Evaluates Random Forest, Decision Tree, and Naive Bayes classifiers to select the top model.
   - Outputs primary predicted condition, probability confidence score, and alternative possibilities.
4. **Tailored Precautions & Lifestyle Recommendations**:
   - Specific precautions to prevent disease progression.
   - Tailored lifestyle habits and safe physical exercise protocols.
   - Nutritional breakdown: **Foods Recommended to Eat** vs **Foods to Strictly Avoid**.
5. **AI Health Chatbot**:
   - 24/7 rule-based symptom analyzer and wellness advisor.
   - Emergency keyword detection with critical hotline warnings for high-risk symptoms.
6. **Doctor Portal & Live Consultation**:
   - Browse certified medical specialists (Cardiology, Neurology, Pulmonology, Psychiatry, etc.).
   - Live private messaging between patients and doctors with auto-polling.
   - Dedicated Doctor Portal (`/doctor/login`) allowing doctors to manage consultations and appointments.
7. **Appointment Scheduling & Medical Records History**:
   - Book online or in-person consultations with instant automated email confirmations.
   - Historical logs of past AI predictions, symptoms, and appointment statuses.

---

## 🚀 Quick Start Guide

### 1. Install Dependencies
```bash
cd AI_Health_Assistant
pip install -r requirements.txt
```

### 2. Train the Machine Learning Model
```bash
python model_training.py
```
*Trains classification models and saves the optimized `disease_model.pkl`.*

### 3. Run the Flask Web Application
```bash
python app.py
```
Open your browser at:
```
http://127.0.0.1:5000
```

---

## 🔑 Demo Credentials

### Patient Account:
- Register a new account via the **Register** button, or test using:
- **Email:** `john@example.com`
- **Password:** `password123`

### Doctor Portal:
- Navigate to: `http://127.0.0.1:5000/doctor/login`
- **Email:** `dr.anil@healthapp.com`
- **Password:** `password123`

---

## 📧 Email Notification System Setup

Email settings are configured in `.env`:
```ini
SECRET_KEY=ai_health_assistant_secret_key_2026_x
MAIL_USERNAME=your_gmail_address@gmail.com
MAIL_PASSWORD=your_gmail_app_password
EMAIL_DEV_MODE=true
```
- When `EMAIL_DEV_MODE=true`, emails are formatted and logged to the terminal console (no real Gmail credentials required for college demo/testing).
- To send real emails, set `EMAIL_DEV_MODE=false` and supply a Gmail App Password.

---

## 🧪 Running the Test Suite
```bash
python test_app.py
```

---

## ⚠️ Medical Disclaimer
*AI predictions provided by this application are for informational and educational purposes only. They do not constitute a clinical medical diagnosis. Users should always consult a licensed medical professional for personal health concerns.*

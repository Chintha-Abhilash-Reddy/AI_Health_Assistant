"""
test_app.py — Automated verification test suite for AI Health Assistant
"""
import unittest
import json
import uuid
from app import app
import database as db
import model_training as ml
import chatbot as ai_bot


class HealthAssistantTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        self.client = app.test_client()
        db.init_db()
        self.test_email = f"test_{uuid.uuid4().hex[:6]}@example.com"
        self.test_password = "securepassword123"

    def test_01_index_page(self):
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"AI Powered Health Assistant", res.data)

    def test_02_registration_and_login(self):
        # Register a test user
        res = self.client.post("/register", data={
            "full_name": "Test Patient",
            "age": "28",
            "gender": "Male",
            "email": self.test_email,
            "phone": "9876543210",
            "password": self.test_password,
            "confirm_password": self.test_password
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Registration successful", res.data)

        # Login test user
        res = self.client.post("/login", data={
            "email": self.test_email,
            "password": self.test_password
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Welcome", res.data)

    def test_03_profile_and_bmi(self):
        with self.client:
            # Register & login
            self.client.post("/register", data={
                "full_name": "Test Patient",
                "age": "28",
                "gender": "Male",
                "email": self.test_email,
                "phone": "9876543210",
                "password": self.test_password,
                "confirm_password": self.test_password
            })
            self.client.post("/login", data={
                "email": self.test_email,
                "password": self.test_password
            })
            # Update Profile
            res = self.client.post("/profile", data={
                "full_name": "Test Patient",
                "age": "29",
                "gender": "Male",
                "phone": "9876543210",
                "height": "180",
                "weight": "75",
                "blood_group": "O+",
                "blood_pressure": "120/80",
                "blood_sugar": "90",
                "heart_rate": "72",
                "body_temperature": "98.6",
                "existing_diseases": "None",
                "allergies": "Dust",
                "current_medications": "None",
                "smoking_habit": "Non-Smoker",
                "alcohol_consumption": "Never",
                "exercise_frequency": "3-4 times/week",
                "sleeping_hours": "8"
            }, follow_redirects=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn(b"Health profile updated", res.data)

    def test_04_symptom_prediction(self):
        with self.client:
            self._login_user()
            # Submit symptoms
            res = self.client.post("/predict", data={
                "fever": "1",
                "headache": "1",
                "cough": "1",
                "duration": "1-2 days",
                "severity": "Moderate",
                "temperature": "100.4"
            }, follow_redirects=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn(b"Analysis Result:", res.data)
            self.assertIn(b"Confidence", res.data)

    def test_05_chatbot_api(self):
        res = self.client.post("/api/chat", json={"message": "I have fever and headache"})
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertIn("response", data)


    def test_06_doctor_login_and_dashboard(self):
        res = self.client.post("/doctor/login", data={
            "email": "dr.anil@healthapp.com",
            "password": "password123"
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Dr. Anil Kumar", res.data)

    def _login_user(self):
        self.client.post("/register", data={
            "full_name": "Test Patient",
            "age": "28",
            "gender": "Male",
            "email": self.test_email,
            "phone": "9876543210",
            "password": self.test_password,
            "confirm_password": self.test_password
        })
        self.client.post("/login", data={
            "email": self.test_email,
            "password": self.test_password
        })

    def test_07_appointment_booking(self):
        with self.client:
            self._login_user()
            res = self.client.post("/appointment", data={
                "doctor_id": "1",
                "appointment_date": "2026-09-01",
                "appointment_time": "10:00 AM",
                "reason": "Regular wellness consultation"
            }, follow_redirects=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn(b"Appointment booked successfully", res.data)

    def test_08_ambulance_sos_dispatch(self):
        with self.client:
            self._login_user()
            res = self.client.post("/ambulance", data={
                "patient_name": "Emergency Patient",
                "patient_age": "45",
                "mobile_number": "9876543210",
                "area_location": "Indiranagar, Bengaluru",
                "emergency_reason": "Acute chest pain"
            }, follow_redirects=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn(b"Ambulance Unit AMB-108 Dispatched", res.data)
            self.assertIn(b"Open Google Maps Direct Route Navigation", res.data)

    def test_09_sms_service(self):
        import sms_service as sms
        result = sms.send_ambulance_dispatch_sms(
            patient_name="Test Patient",
            patient_age="30",
            mobile_number="9876543210",
            area_location="Koramangala, Bengaluru",
            emergency_reason="Difficulty breathing",
            maps_url="https://www.google.com/maps/dir/?api=1&destination=Koramangala"
        )
        self.assertTrue(result)

    def test_10_prediction_sms_tablets_and_report(self):
        with self.client:
            self._login_user()
            res = self.client.post("/predict", data={
                "cold": "1",
                "cough": "1",
                "headache": "1",
                "duration": "24 hours",
                "mobile_number": "9876543210",
                "send_sms_report": "1",
                "send_email_report": "1"
            }, follow_redirects=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn(b"Suggested Tablets", res.data)
            self.assertIn(b"Report", res.data)

            # Test report route
            pred = db.query_one("SELECT id FROM predictions ORDER BY id DESC LIMIT 1")
            self.assertIsNotNone(pred)
            report_res = self.client.get(f"/report/{pred['id']}")
            self.assertEqual(report_res.status_code, 200)
            self.assertIn(b"Report", report_res.data)

    def test_11_duration_and_whatsapp_and_camera_report(self):
        with self.client:
            self._login_user()
            res = self.client.post("/predict", data={
                "chest_pain": "1",
                "breathing_difficulty": "1",
                "duration": "24 hours",
                "severity": "Severe",
                "temperature": "103.5",
                "mobile_number": "9876543210",
                "send_sms_report": "1",
                "send_whatsapp_report": "1",
                "camera_image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEASABIAAD/2wBDAP//////////////////////////////////////////////////////////////////////////////////////wgALCAABAAEBAREA/8QAFBABAAAAAAAAAAAAAAAAAAAAAP/aAAgBAQABPxA="
            }, follow_redirects=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn(b"CRITICAL HEALTH RISK DETECTED", res.data)
            self.assertIn(b"WhatsApp", res.data)
            self.assertIn(b"Duration: 24 hours", res.data)
            self.assertIn(b"How to Take", res.data)


    def test_12_public_rest_apis(self):
        # 1. Health API
        res = self.client.get("/api/health")
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data["status"], "healthy")

        # 2. Symptoms API
        res = self.client.get("/api/symptoms")
        self.assertEqual(res.status_code, 200)
        sym_data = json.loads(res.data)
        self.assertIn("categories", sym_data)

        # 3. Predict API
        res = self.client.post("/api/predict", json={
            "symptoms": ["cough", "throat_irritation", "fever"],
            "duration": "2 days",
            "severity": "Mild"
        })
        self.assertEqual(res.status_code, 200)
        pred_data = json.loads(res.data)
        self.assertTrue(pred_data["success"])
        self.assertIn("predicted_disease", pred_data)
        self.assertIn("tablets", pred_data)

        # 4. Ambulance API
        res = self.client.post("/api/ambulance", json={
            "patient_name": "Emergency Test Patient",
            "patient_age": "45",
            "mobile_number": "9876543210",
            "area_location": "Green Park Sector 12",
            "emergency_reason": "Acute Chest Pain"
        })
        self.assertEqual(res.status_code, 201)
        amb_data = json.loads(res.data)
        self.assertTrue(amb_data["success"])
        self.assertEqual(amb_data["status"], "Dispatched")

        # 5. Doctors API
        res = self.client.get("/api/doctors")
        self.assertEqual(res.status_code, 200)
        doc_data = json.loads(res.data)
        self.assertTrue(doc_data["success"])
        self.assertGreater(len(doc_data["doctors"]), 0)

        # 6. Deep Links verification
        res_asset = self.client.get("/.well-known/assetlinks.json")
        self.assertEqual(res_asset.status_code, 200)
        res_apple = self.client.get("/.well-known/apple-app-site-association")
        self.assertEqual(res_apple.status_code, 200)

        # 7. Download portal page
        res_down = self.client.get("/download")
        self.assertEqual(res_down.status_code, 200)
        self.assertIn(b"Download AI Health Assistant", res_down.data)


if __name__ == "__main__":
    unittest.main()



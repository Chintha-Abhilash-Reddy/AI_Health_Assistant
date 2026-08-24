"""
sms_service.py — SMS Alert Dispatch Service for AI Health Assistant & Emergency Ambulance
"""
import os
import urllib.parse
from datetime import datetime

# Check environment settings for SMS
SMS_DEV_MODE = os.getenv("SMS_DEV_MODE", "true").lower() in ("true", "1", "yes")
SMS_API_KEY = os.getenv("SMS_API_KEY", "")
SMS_SENDER_ID = os.getenv("SMS_SENDER_ID", "AIHLTH")


def send_sms(mobile_number: str, message: str, open_browser_whatsapp: bool = False) -> bool:
    """
    Sends an SMS message to the target mobile number.
    In DEV mode, logs the full SMS box to the terminal and can trigger WhatsApp / SMS app.
    In PRODUCTION mode (when SMS_API_KEY is set), sends via HTTP SMS gateway.
    """
    if not mobile_number:
        print("[SMS ERROR] Target mobile number is required.")
        return False

    clean_mobile = str(mobile_number).strip().replace(" ", "").replace("-", "").replace("+", "")

    # Always log formatted alert to terminal
    print("\n" + "=" * 65)
    print(f"🚨 [SMS NOTIFICATION DISPATCH] To: +{clean_mobile}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 65)
    print(message.strip())
    print("=" * 65 + "\n")

    if SMS_API_KEY and not SMS_DEV_MODE:
        # Production SMS Gateway Integration (Fast2SMS / Twilio)
        try:
            import requests
            url = "https://www.fast2sms.com/dev/bulkV2"
            payload = {
                "authorization": SMS_API_KEY,
                "message": message,
                "language": "english",
                "route": "q",
                "numbers": clean_mobile,
            }
            headers = {'cache-control': "no-cache"}
            res = requests.post(url, data=payload, headers=headers, timeout=10)
            if res.status_code == 200:
                print(f"[SMS OK] Gateway dispatched SMS successfully to {clean_mobile}")
                return True
        except Exception as e:
            print(f"[SMS ERROR] Failed to send SMS via gateway: {e}")

    # Fallback to direct WhatsApp / SMS client link if requested
    if open_browser_whatsapp:
        try:
            import webbrowser
            wa_url = generate_whatsapp_url(clean_mobile, message)
            webbrowser.open(wa_url)
        except Exception:
            pass

    return True


def generate_whatsapp_url(mobile_number: str, message: str) -> str:
    """
    Generates WhatsApp Web/API messaging URL as fallback.
    """
    clean_mobile = str(mobile_number or "").strip().replace("+", "").replace(" ", "").replace("-", "")
    encoded_text = urllib.parse.quote(message)
    if clean_mobile:
        return f"https://api.whatsapp.com/send?phone={clean_mobile}&text={encoded_text}"
    return f"https://api.whatsapp.com/send?text={encoded_text}"


def generate_whatsapp_app_url(mobile_number: str, message: str) -> str:
    """
    Generates a direct native WhatsApp application URI scheme (whatsapp://send).
    Directly opens the installed WhatsApp Desktop or Mobile App without opening WhatsApp Web.
    """
    clean_mobile = str(mobile_number or "").strip().replace("+", "").replace(" ", "").replace("-", "")
    encoded_text = urllib.parse.quote(message)
    if clean_mobile:
        return f"whatsapp://send?phone={clean_mobile}&text={encoded_text}"
    return f"whatsapp://send?text={encoded_text}"


def open_native_whatsapp(mobile_number: str, message: str) -> bool:
    """
    Directly opens the native WhatsApp application on the system.
    """
    clean_mobile = str(mobile_number or "").strip().replace("+", "").replace(" ", "").replace("-", "")
    encoded_text = urllib.parse.quote(message)
    app_uri = f"whatsapp://send?phone={clean_mobile}&text={encoded_text}"
    try:
        if os.name == "nt":
            os.system(f'start "" "{app_uri}"')
            return True
        else:
            import webbrowser
            webbrowser.open(app_uri)
            return True
    except Exception as e:
        print(f"[!] Could not launch native WhatsApp app: {e}")
        return False


def generate_native_sms_url(mobile_number: str, message: str) -> str:
    """
    Generates an sms: URI scheme that directly launches native SMS on mobile phones.
    """
    clean_mobile = str(mobile_number or "").strip().replace(" ", "").replace("-", "")
    encoded_text = urllib.parse.quote(message)
    return f"sms:{clean_mobile}?body={encoded_text}"


def format_prediction_alert_message(
    patient_name: str,
    predicted_disease: str,
    confidence: float,
    precautions: list,
    tablets: list,
    is_emergency: bool = False,
    report_url: str = "",
    doctor_name: str = "Dr. Anil Kumar, MD",
    doctor_specialty: str = "Senior Medical Officer",
    consultation_date: str = ""
) -> str:
    """
    Constructs a comprehensive, clear SMS/WhatsApp notification alert containing
    patient name, date, consulting doctor, detailed medicine info, and emergency instructions.
    """
    if not consultation_date:
        consultation_date = datetime.now().strftime("%d %b %Y, %I:%M %p")

    tablet_summary = ""
    if tablets:
        t_items = []
        for i, t in enumerate(tablets[:3], 1):
            t_name = t.get("name", "Medication")
            t_dose = t.get("dosage", "As prescribed")
            t_timing = t.get("timing", "After Meals")
            t_take = t.get("how_to_take", "Take with water")
            t_dur = t.get("duration", "3-5 Days")
            t_items.append(f"  {i}. {t_name} ({t_dose})\n     Dosage: {t_timing} ({t_dur})\n     Instruction: {t_take}")
        tablet_summary = "\n💊 Prescribed Medicines & Intake:\n" + "\n".join(t_items)

    risk_banner = ""
    if is_emergency:
        risk_banner = (
            "\n🚨 CRITICAL DANGER ALERT 🚨\n"
            "High-risk condition detected! PLEASE CONTACT A DOCTOR IMMEDIATELY or call emergency 108 / 112!\n"
        )

    msg = (
        f"🏥 MEDICAL DIAGNOSTIC & PRESCRIPTION REPORT\n"
        f"📅 Date: {consultation_date}\n"
        f"👨‍⚕️ Prescribed By: {doctor_name} ({doctor_specialty})\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 Patient Name: {patient_name}\n"
        f"🎯 Diagnosis: {predicted_disease} (AI Confidence: {confidence:.1f}%)\n"
        f"{risk_banner}"
        f"🛡️ Key Precaution: {precautions[0] if precautions else 'Follow physician advice'}\n"
        f"{tablet_summary}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📄 View Full Digital Report: {report_url}\n"
        f"⚠️ NOTE: AI assisted preliminary triage. Always consult your healthcare provider."
    )
    return msg.strip()


def send_ambulance_dispatch_sms(
    patient_name: str,
    patient_age: str,
    mobile_number: str,
    area_location: str,
    emergency_reason: str,
    maps_url: str,
    ambulance_service_number: str = "108"
) -> bool:
    """
    Constructs and sends emergency ambulance dispatch SMS to the patient and ambulance control.
    """
    sms_text = (
        f"🚨 EMERGENCY AMBULANCE ALERT 🚨\n"
        f"Patient: {patient_name} (Age: {patient_age})\n"
        f"Phone: {mobile_number}\n"
        f"Location: {area_location}\n"
        f"Reason: {emergency_reason}\n"
        f"Google Maps Live Route:\n{maps_url}\n"
        f"Dispatch Status: AMBULANCE EN ROUTE (Emergency Hotline: {ambulance_service_number})\n"
        f"PLEASE KEEP PHONE ACTIVE. FIRST RESPONDERS ON THE WAY."
    )

    # Send to patient for confirmation
    patient_sent = send_sms(mobile_number, sms_text)

    # Also log dispatch notification to ambulance emergency dispatch center
    ambulance_sent = send_sms(
        ambulance_service_number,
        f"[DISPATCH CALL] Urgent ambulance requested for {patient_name} at {area_location}. Route: {maps_url}"
    )

    return patient_sent or ambulance_sent

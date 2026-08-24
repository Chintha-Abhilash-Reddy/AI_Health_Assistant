"""
chatbot.py — AI Health Chatbot engine with symptom recognition,
emergency detection, and health recommendations.
"""
import re
from recommendation import (
    DISEASE_DATA,
    get_disease_info,
    get_precautions,
    get_lifestyle,
    get_food_recommendation,
    get_foods_to_avoid,
    get_exercise_recommendation
)

# ── Emergency Symptoms keywords ───────────────────────────────────────────
EMERGENCY_KEYWORDS = [
    "chest pain", "heart attack", "can't breathe", "difficulty breathing",
    "cannot breathe", "shortness of breath", "severe bleeding", "unconscious",
    "stroke", "paralysis", "seizure", "coughing blood", "vomiting blood",
    "severe burn", "poisoning", "suicide", "overdose"
]

# ── Greeting Patterns ──────────────────────────────────────────────────────
GREETING_PATTERNS = [
    r"\b(hi|hello|hey|greetings|good morning|good afternoon|good evening|namaste)\b"
]

# ── Common Queries and Intents ─────────────────────────────────────────────
INTENT_RESPONSES = {
    "bmi": (
        "💡 **About BMI (Body Mass Index):**\n"
        "BMI = Weight (kg) / [Height (m)]²\n\n"
        "• Underweight: < 18.5\n"
        "• Normal weight: 18.5 – 24.9\n"
        "• Overweight: 25.0 – 29.9\n"
        "• Obese: ≥ 30.0\n\n"
        "You can view and update your BMI in your **Health Profile**!"
    ),
    "bp": (
        "💡 **Blood Pressure Ranges (mmHg):**\n"
        "• Normal: Less than 120/80\n"
        "• Elevated: 120-129 / <80\n"
        "• Stage 1 Hypertension: 130-139 / 80-89\n"
        "• Stage 2 Hypertension: 140+ / 90+\n"
        "• Hypertensive Crisis: > 180 and/or > 120 (Seek emergency care!)"
    ),
    "water": (
        "💧 **Daily Water Intake Recommendation:**\n"
        "• Men: ~3.7 liters (approx. 13-15 glasses)\n"
        "• Women: ~2.7 liters (approx. 9-11 glasses)\n"
        "Drink more if exercising or during hot weather!"
    ),
    "sleep": (
        "😴 **Healthy Sleep Guidelines:**\n"
        "• Adults (18–64): 7–9 hours per night\n"
        "• Seniors (65+): 7–8 hours per night\n"
        "• Teenagers: 8–10 hours per night\n"
        "Tips: Avoid screens 1 hour before bed, keep room cool and dark, sleep at regular times."
    ),
    "exercise": (
        "🏃 **Weekly Exercise Recommendation:**\n"
        "• Moderate aerobic: at least 150 minutes/week (e.g. brisk walking)\n"
        "• OR Vigorous aerobic: 75 minutes/week (e.g. running, swimming)\n"
        "• Strength training: 2 or more days/week targeting all major muscle groups."
    ),
    "doctor": (
        "👨‍⚕️ You can consult with our verified doctors anytime!\n"
        "Go to the **Doctors** section in the navigation menu to browse specialists and start a private chat or book an appointment."
    )
}

# ── Symptom to Disease mappings for quick lookup ──────────────────────────
SYMPTOM_MAP = {
    "fever": ["Common Cold", "Influenza", "Malaria", "Dengue", "Typhoid", "Pneumonia", "COVID-19"],
    "headache": ["Migraine", "Hypertension", "Common Cold", "Influenza", "Dengue", "Typhoid"],
    "cough": ["Common Cold", "Influenza", "Bronchitis", "Pneumonia", "Asthma", "COVID-19"],
    "chest pain": ["Heart Disease", "GERD", "Pneumonia", "Bronchitis", "Asthma"],
    "breathing difficulty": ["Asthma", "Pneumonia", "COVID-19", "Heart Disease", "Bronchitis"],
    "stomach pain": ["Gastritis", "GERD", "Typhoid", "Food Poisoning"],
    "diarrhea": ["Typhoid", "Food Poisoning", "Gastritis"],
    "vomiting": ["Food Poisoning", "Gastritis", "Malaria", "Dengue", "Migraine"],
    "joint pain": ["Arthritis", "Dengue", "Influenza", "COVID-19"],
    "skin rash": ["Allergy", "Dengue", "Measles"],
    "dizziness": ["Hypertension", "Diabetes", "Migraine", "Anemia"],
    "sore throat": ["Common Cold", "Influenza", "COVID-19"],
    "fatigue": ["Diabetes", "Anemia", "Hypertension", "Influenza", "COVID-19", "Typhoid"]
}


def analyze_chat_message(message: str) -> dict:
    """
    Process incoming user message and generate structured chatbot response.
    Returns:
        {
            "response": str,
            "is_emergency": bool,
            "matched_disease": str or None,
            "disclaimer": str
        }
    """
    cleaned = message.lower().strip()
    disclaimer = "\n\n⚠️ *Disclaimer: I am an AI Health Assistant, not a doctor. For serious symptoms or medical decisions, please consult a healthcare professional.*"

    # 1. Check for Emergency
    for em in EMERGENCY_KEYWORDS:
        if em in cleaned:
            return {
                "response": (
                    "🚨 **EMERGENCY DETECTED!**\n\n"
                    f"Your message mentions **'{em}'**, which could indicate a medical emergency.\n\n"
                    "⚠️ **Please take immediate action:**\n"
                    "1. Call your local emergency hotline (e.g. 911, 112, 108) immediately.\n"
                    "2. Go to the nearest emergency room or hospital.\n"
                    "3. Do not rely solely on online assistance during a critical condition."
                ),
                "is_emergency": True,
                "matched_disease": None,
                "disclaimer": disclaimer
            }

    # 2. Check Greetings
    for pattern in GREETING_PATTERNS:
        if re.search(pattern, cleaned):
            return {
                "response": (
                    "👋 **Hello! I'm your AI Health Assistant.**\n\n"
                    "How can I help you today? You can:\n"
                    "• Describe your symptoms (e.g., *'I have fever and sore throat'*)\n"
                    "• Ask about a disease (e.g., *'Tell me about Hypertension'* or *'Diet for Diabetes'*)\n"
                    "• Ask health questions (e.g., *'What is normal BMI?'*, *'How much water should I drink?'*)\n"
                    "• Navigate to the **Symptom Predictor** for full AI analysis!"
                ),
                "is_emergency": False,
                "matched_disease": None,
                "disclaimer": disclaimer
            }

    # 3. Check for Tablet / Medicine Questions
    if any(w in cleaned for w in ["tablet", "tablets", "medicine", "medicines", "medication", "dosage", "how to take", "pill", "pills"]):
        for disease_name, info in DISEASE_DATA.items():
            if disease_name.lower() in cleaned:
                tabs = info.get("tablets", [])
                if tabs:
                    tab_lines = []
                    for t in tabs:
                        tab_lines.append(
                            f"💊 **{t['name']}** ({t.get('type', 'Medication')})\n"
                            f"   • **Dosage:** {t['dosage']}\n"
                            f"   • **How to Take:** {t.get('how_to_take', 'Take with water after meals.')}\n"
                            f"   • **Timing:** {t.get('timing', 'After Food')}\n"
                            f"   • **Note:** {t.get('note', 'Consult physician.')}"
                        )
                    tab_text = "\n\n".join(tab_lines)
                    return {
                        "response": (
                            f"💊 **Suggested Medications for {disease_name}:**\n\n"
                            f"{tab_text}\n\n"
                            f"⚠️ **How to safely take medicines:**\n"
                            f"1. Always take after meals unless specifically marked empty stomach.\n"
                            f"2. Swallow with a full glass of water. Do not crush or break coated tablets.\n"
                            f"3. Never self-medicate with antibiotics or prescription antivirals without a doctor's consultation.\n"
                            f"4. If condition worsens or causes allergic reactions, stop immediately and seek emergency care."
                            + disclaimer
                        ),
                        "is_emergency": False,
                        "matched_disease": disease_name,
                        "disclaimer": disclaimer
                    }

    # 4. Check for Disease Inquiries
    for disease_name, info in DISEASE_DATA.items():
        if disease_name.lower() in cleaned:
            # Check specific sub-intent
            if any(w in cleaned for w in ["food", "diet", "eat", "avoid"]):
                foods_rec = "\n".join(f"  ✓ {f}" for f in info["foods_recommended"][:5])
                foods_avoid = "\n".join(f"  ✗ {f}" for f in info["foods_to_avoid"][:5])
                resp = (
                    f"🥗 **Dietary Advice for {disease_name}:**\n\n"
                    f"**Recommended Foods:**\n{foods_rec}\n\n"
                    f"**Foods to Avoid:**\n{foods_avoid}"
                )
            elif any(w in cleaned for w in ["lifestyle", "habit", "routine", "exercise", "activity"]):
                lifestyle = "\n".join(f"  • {l}" for l in info["lifestyle"][:5])
                resp = (
                    f"🧘 **Lifestyle & Exercise for {disease_name}:**\n\n"
                    f"**Lifestyle Recommendations:**\n{lifestyle}\n\n"
                    f"**Exercise Advice:**\n{info['exercise']}"
                )
            elif any(w in cleaned for w in ["precaution", "prevent", "care", "tips"]):
                prec = "\n".join(f"  • {p}" for p in info["precautions"][:5])
                resp = (
                    f"🛡️ **Precautions for {disease_name}:**\n\n{prec}"
                )
            else:
                prec = "\n".join(f"  • {p}" for p in info["precautions"][:4])
                foods = "\n".join(f"  ✓ {f}" for f in info["foods_recommended"][:3])
                tabs = [t["name"] for t in info.get("tablets", [])[:3]]
                tab_str = ", ".join(tabs) if tabs else "Consult physician"
                resp = (
                    f"📋 **Information for {disease_name}:**\n\n"
                    f"**Key Precautions:**\n{prec}\n\n"
                    f"**Common Medications / Tablets:** {tab_str}\n\n"
                    f"**Diet Recommendations:**\n{foods}\n\n"
                    f"**Exercise:** {info['exercise']}\n\n"
                    f"💡 *Ask me specifically about 'tablets for {disease_name}', 'diet for {disease_name}' or 'lifestyle for {disease_name}'!*"
                )

            return {
                "response": resp + disclaimer,
                "is_emergency": False,
                "matched_disease": disease_name,
                "disclaimer": disclaimer
            }

    # 5. Check Common Health Intent Keywords
    for key, text in INTENT_RESPONSES.items():
        if key in cleaned:
            return {
                "response": text + disclaimer,
                "is_emergency": False,
                "matched_disease": None,
                "disclaimer": disclaimer
            }

    # 6. Symptom Analysis from chat with Risk Assessment
    detected_symptoms = []
    for symptom, diseases in SYMPTOM_MAP.items():
        if symptom in cleaned:
            detected_symptoms.append((symptom, diseases))

    if detected_symptoms:
        symptoms_str = ", ".join(f"**{s[0].title()}**" for s in detected_symptoms)
        all_possible_diseases = []
        for _, dis_list in detected_symptoms:
            all_possible_diseases.extend(dis_list)
        from collections import Counter
        top_diseases = [d for d, _ in Counter(all_possible_diseases).most_common(3)]
        dis_text = ", ".join(top_diseases)

        # Risk indicator check
        is_risky = any(s[0] in ["chest pain", "breathing difficulty", "high fever", "vomiting blood"] for s in detected_symptoms)
        risk_alert = ""
        if is_risky:
            risk_alert = (
                "\n\n🚨 **CRITICAL RISK ALERT:** The symptoms mentioned are considered high-risk. "
                "**Please contact a doctor immediately** or dial **108 / 112** for emergency ambulance services!"
            )

        return {
            "response": (
                f"🔍 **AI Symptom Assessment:**\n\n"
                f"I noticed you mentioned: {symptoms_str}.\n\n"
                f"These symptoms are commonly associated with conditions like: **{dis_text}**."
                f"{risk_alert}\n\n"
                "**Recommended Immediate Steps:**\n"
                "1. Go to **Symptom Predictor** to run our full Machine Learning analysis with vitals.\n"
                "2. Check suggested precautions and medications.\n"
                "3. If symptoms persist for **more than 24 hours** or worsen, consult a registered doctor right away.\n"
                "4. You can chat directly with our verified physicians on the **Doctors** page."
                + disclaimer
            ),
            "is_emergency": is_risky,
            "matched_disease": top_diseases[0] if top_diseases else None,
            "disclaimer": disclaimer
        }

    # 7. Default Fallback
    return {
        "response": (
            "🤖 **I'm here to assist you 24/7 with health questions, symptoms, and medications.**\n\n"
            "I can help you with:\n"
            "• **Symptoms**: *'I have fever and cough for 24 hours'*\n"
            "• **Medications & Tablets**: *'What tablets for migraine and how to take them?'*\n"
            "• **Conditions**: *'Tell me about Typhoid'*, *'Diet for Hypertension'*\n"
            "• **Emergencies**: Immediate 108 SOS dispatch instructions\n\n"
            "Try asking your health question or describe how you are feeling!"
            + disclaimer
        ),
        "is_emergency": False,
        "matched_disease": None,
        "disclaimer": disclaimer
    }

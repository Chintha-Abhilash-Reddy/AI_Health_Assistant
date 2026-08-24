"""
desktop_app.py — Native Python Desktop Application for AI Health Assistant
Built with Tkinter, Modern Theming, NumPy Vectorization, SQLite, and Google Maps & SMS Emergency Response.
"""

import os
import sys
import json
import webbrowser
import urllib.parse
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import numpy as np

# Internal application modules
import database as db
import email_service as mail
import sms_service as sms
import recommendation as rec
import chatbot as ai_bot
import model_training as ml
from werkzeug.security import generate_password_hash, check_password_hash


# ── Color Palette & Styles (Clean Medical White & Stethoscope Cyan/Teal) ───────
PALETTE = {
    "bg_main": "#F8FAFC",          # Ultra clean medical white/slate
    "bg_card": "#FFFFFF",          # Pure white card background
    "bg_card_subtle": "#F1F5F9",   # Soft subtle grey
    "primary": "#0D9488",          # Medical Teal / Cyan
    "primary_dark": "#0F766E",
    "primary_light": "#CCFBF1",
    "secondary": "#2563EB",        # Royal Medical Blue
    "danger": "#DC2626",           # Emergency Crimson Red
    "danger_light": "#FEE2E2",
    "success": "#16A34A",          # Medical Green
    "success_light": "#DCFCE7",
    "warning": "#D97706",          # Amber
    "text_dark": "#0F172A",        # Deep slate text
    "text_muted": "#64748B",       # Muted slate text
    "border": "#E2E8F0"            # Soft border
}


class AIHealthAssistantDesktop(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AI Powered Health Assistant & Emergency Ambulance Portal")
        self.geometry("1100x750")
        self.minsize(950, 650)
        self.configure(bg=PALETTE["bg_main"])

        # Initialize backend DB & ML
        db.init_db()
        if not os.path.exists(ml.MODEL_PATH):
            print("[+] Training AI Model for Desktop App...")
            ml.train_models()

        # Session state
        self.current_user = None  # {id, full_name, email, age, phone, role}

        # Apply ttk styles
        self._setup_styles()

        # Container frame
        self.container = tk.Frame(self, bg=PALETTE["bg_main"])
        self.container.pack(fill="both", expand=True)

        # Show initial authentication screen
        self.show_auth_screen()

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TNotebook", background=PALETTE["bg_main"], borderwidth=0)
        style.configure("TNotebook.Tab", background=PALETTE["bg_card_subtle"], foreground=PALETTE["text_dark"],
                        padding=[16, 8], font=("Segoe UI", 10, "bold"))
        style.map("TNotebook.Tab",
                  background=[("selected", PALETTE["primary"])],
                  foreground=[("selected", "#FFFFFF")])

        style.configure("TFrame", background=PALETTE["bg_main"])
        style.configure("Card.TFrame", background=PALETTE["bg_card"], relief="solid", borderwidth=1)
        style.configure("TLabel", background=PALETTE["bg_card"], foreground=PALETTE["text_dark"], font=("Segoe UI", 10))
        style.configure("Header.TLabel", background=PALETTE["bg_card"], foreground=PALETTE["primary_dark"], font=("Segoe UI", 16, "bold"))
        style.configure("Title.TLabel", background=PALETTE["bg_main"], foreground=PALETTE["primary_dark"], font=("Segoe UI", 20, "bold"))
        style.configure("Subtitle.TLabel", background=PALETTE["bg_main"], foreground=PALETTE["text_muted"], font=("Segoe UI", 10))

    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    # ──────────────────────────────────────────────────────────────────────────
    # 1. AUTHENTICATION (Login / Register)
    # ──────────────────────────────────────────────────────────────────────────
    def show_auth_screen(self):
        self.clear_container()

        # Main background frame
        auth_frame = tk.Frame(self.container, bg=PALETTE["bg_main"])
        auth_frame.pack(fill="both", expand=True)

        # Top Banner with Stethoscope Brand Icon
        header_banner = tk.Frame(auth_frame, bg=PALETTE["bg_card"], height=90, highlightbackground=PALETTE["border"], highlightthickness=1)
        header_banner.pack(fill="x", side="top", pady=(0, 20))

        brand_lbl = tk.Label(header_banner, text="🩺 AI POWERED HEALTH ASSISTANT", font=("Segoe UI", 18, "bold"),
                             fg=PALETTE["primary_dark"], bg=PALETTE["bg_card"])
        brand_lbl.pack(side="left", padx=25, pady=18)

        sub_brand_lbl = tk.Label(header_banner, text="Disease Prediction • Diet & Lifestyle • Emergency Ambulance SOS",
                                 font=("Segoe UI", 10), fg=PALETTE["text_muted"], bg=PALETTE["bg_card"])
        sub_brand_lbl.pack(side="left", padx=5, pady=22)

        # Center Card Container
        center_card = tk.Frame(auth_frame, bg=PALETTE["bg_card"], bd=1, relief="solid", highlightbackground=PALETTE["border"])
        center_card.place(relx=0.5, rely=0.53, anchor="center", width=520, height=540)

        # Notebook tabs: Login vs Register
        auth_tabs = ttk.Notebook(center_card)
        auth_tabs.pack(fill="both", expand=True, padx=20, pady=20)

        login_tab = tk.Frame(auth_tabs, bg=PALETTE["bg_card"])
        register_tab = tk.Frame(auth_tabs, bg=PALETTE["bg_card"])

        auth_tabs.add(login_tab, text="  🔑 Sign In  ")
        auth_tabs.add(register_tab, text="  📝 Register Account  ")

        # ── Sign In View ──
        tk.Label(login_tab, text="Welcome Back", font=("Segoe UI", 16, "bold"), fg=PALETTE["text_dark"], bg=PALETTE["bg_card"]).pack(anchor="w", pady=(10, 2))
        tk.Label(login_tab, text="Access your health records and medical assistant", font=("Segoe UI", 9), fg=PALETTE["text_muted"], bg=PALETTE["bg_card"]).pack(anchor="w", pady=(0, 15))

        tk.Label(login_tab, text="Email Address:", font=("Segoe UI", 10, "bold"), fg=PALETTE["text_dark"], bg=PALETTE["bg_card"]).pack(anchor="w", pady=(5, 2))
        login_email_entry = tk.Entry(login_tab, font=("Segoe UI", 11), bg="#F8FAFC", relief="solid", bd=1)
        login_email_entry.pack(fill="x", ipady=6, pady=(0, 10))
        login_email_entry.insert(0, "john@example.com")

        tk.Label(login_tab, text="Password:", font=("Segoe UI", 10, "bold"), fg=PALETTE["text_dark"], bg=PALETTE["bg_card"]).pack(anchor="w", pady=(5, 2))
        login_pwd_entry = tk.Entry(login_tab, font=("Segoe UI", 11), show="•", bg="#F8FAFC", relief="solid", bd=1)
        login_pwd_entry.pack(fill="x", ipady=6, pady=(0, 15))
        login_pwd_entry.insert(0, "password123")

        role_var = tk.StringVar(value="patient")
        role_frame = tk.Frame(login_tab, bg=PALETTE["bg_card"])
        role_frame.pack(fill="x", pady=(0, 15))
        tk.Radiobutton(role_frame, text="Patient Account", variable=role_var, value="patient", bg=PALETTE["bg_card"], fg=PALETTE["text_dark"], font=("Segoe UI", 10)).pack(side="left", padx=(0, 15))
        tk.Radiobutton(role_frame, text="Doctor Account", variable=role_var, value="doctor", bg=PALETTE["bg_card"], fg=PALETTE["text_dark"], font=("Segoe UI", 10)).pack(side="left")

        def handle_login():
            email = login_email_entry.get().strip()
            pwd = login_pwd_entry.get().strip()
            role = role_var.get()

            if not email or not pwd:
                messagebox.showerror("Validation Error", "Please provide email and password.")
                return

            if role == "doctor":
                doc = db.query_one("SELECT * FROM doctors WHERE email = ?", (email,))
                if doc and check_password_hash(doc["password_hash"], pwd):
                    self.current_user = {
                        "id": doc["id"], "full_name": doc["name"], "email": doc["email"],
                        "role": "doctor", "specialization": doc["specialization"]
                    }
                    messagebox.showinfo("Doctor Login", f"Welcome Dr. {doc['name']}!")
                    self.show_main_dashboard()
                else:
                    messagebox.showerror("Login Failed", "Invalid doctor email or password.")
            else:
                user = db.query_one("SELECT * FROM users WHERE email = ?", (email,))
                if user and check_password_hash(user["password_hash"], pwd):
                    self.current_user = {
                        "id": user["id"], "full_name": user["full_name"], "email": user["email"],
                        "age": user["age"], "phone": user["phone"], "role": "patient"
                    }
                    messagebox.showinfo("Login Success", f"Welcome, {user['full_name']}!")
                    self.show_main_dashboard()
                else:
                    messagebox.showerror("Login Failed", "Invalid patient email or password.")

        btn_login = tk.Button(login_tab, text="Sign In to Dashboard", font=("Segoe UI", 11, "bold"),
                              bg=PALETTE["primary"], fg="#FFFFFF", activebackground=PALETTE["primary_dark"],
                              activeforeground="#FFFFFF", relief="flat", cursor="hand2", command=handle_login)
        btn_login.pack(fill="x", ipady=8, pady=10)

        # ── Registration View ──
        tk.Label(register_tab, text="Create New Patient Account", font=("Segoe UI", 14, "bold"), fg=PALETTE["text_dark"], bg=PALETTE["bg_card"]).pack(anchor="w", pady=(5, 2))

        reg_name = tk.Entry(register_tab, font=("Segoe UI", 10), bg="#F8FAFC", relief="solid", bd=1)
        reg_age = tk.Entry(register_tab, font=("Segoe UI", 10), bg="#F8FAFC", relief="solid", bd=1)
        reg_phone = tk.Entry(register_tab, font=("Segoe UI", 10), bg="#F8FAFC", relief="solid", bd=1)
        reg_email = tk.Entry(register_tab, font=("Segoe UI", 10), bg="#F8FAFC", relief="solid", bd=1)
        reg_pwd = tk.Entry(register_tab, font=("Segoe UI", 10), show="•", bg="#F8FAFC", relief="solid", bd=1)

        for lbl, entry, default in [
            ("Full Name:", reg_name, "Demo Patient"),
            ("Age:", reg_age, "29"),
            ("Mobile Phone Number:", reg_phone, "9876543210"),
            ("Email Address:", reg_email, "patient@example.com"),
            ("Password:", reg_pwd, "password123")
        ]:
            tk.Label(register_tab, text=lbl, font=("Segoe UI", 9, "bold"), fg=PALETTE["text_dark"], bg=PALETTE["bg_card"]).pack(anchor="w", pady=(2, 0))
            entry.pack(fill="x", ipady=3, pady=(0, 4))
            entry.insert(0, default)

        def handle_register():
            name = reg_name.get().strip()
            age = reg_age.get().strip()
            phone = reg_phone.get().strip()
            email = reg_email.get().strip()
            pwd = reg_pwd.get().strip()

            if not all([name, age, phone, email, pwd]):
                messagebox.showerror("Error", "All registration fields are required.")
                return

            if db.query_one("SELECT id FROM users WHERE email = ?", (email,)):
                messagebox.showwarning("Account Exists", "An account with this email already exists.")
                return

            hashed = generate_password_hash(pwd)
            uid = db.execute(
                "INSERT INTO users (full_name, age, gender, email, phone, password_hash) VALUES (?, ?, ?, ?, ?, ?)",
                (name, int(age) if age.isdigit() else 25, "Other", email, phone, hashed)
            )
            # Create default profile
            db.execute("INSERT OR IGNORE INTO health_profiles (user_id) VALUES (?)", (uid,))
            # Send welcome email and SMS
            mail.send_welcome_email(email, name)
            sms.send_sms(phone, f"Welcome to AI Health Assistant, {name}! Your account is now active.")

            messagebox.showinfo("Success", "Account registered successfully! You can now sign in.")
            auth_tabs.select(login_tab)

        btn_reg = tk.Button(register_tab, text="Create Account", font=("Segoe UI", 10, "bold"),
                            bg=PALETTE["secondary"], fg="#FFFFFF", activebackground="#1D4ED8",
                            relief="flat", cursor="hand2", command=handle_register)
        btn_reg.pack(fill="x", ipady=6, pady=8)

    # ──────────────────────────────────────────────────────────────────────────
    # 2. MAIN DASHBOARD WITH ALL MODULES
    # ──────────────────────────────────────────────────────────────────────────
    def show_main_dashboard(self):
        self.clear_container()

        # Top Navigation Header
        top_bar = tk.Frame(self.container, bg=PALETTE["bg_card"], height=65, highlightbackground=PALETTE["border"], highlightthickness=1)
        top_bar.pack(fill="x", side="top")

        # Brand + Stethoscope Icon
        brand_frame = tk.Frame(top_bar, bg=PALETTE["bg_card"])
        brand_frame.pack(side="left", padx=20, pady=12)
        tk.Label(brand_frame, text="🩺 AI Health Assistant", font=("Segoe UI", 15, "bold"),
                 fg=PALETTE["primary_dark"], bg=PALETTE["bg_card"]).pack(side="left")

        # Quick Emergency SOS Button in Header
        sos_btn = tk.Button(top_bar, text="🚨 EMERGENCY AMBULANCE SOS (108)", font=("Segoe UI", 10, "bold"),
                            bg=PALETTE["danger"], fg="#FFFFFF", activebackground="#B91C1C",
                            activeforeground="#FFFFFF", relief="flat", cursor="hand2",
                            padx=15, pady=4, command=lambda: self.notebook.select(self.tab_ambulance))
        sos_btn.pack(side="left", padx=30, pady=12)

        # User Info & Logout
        user_frame = tk.Frame(top_bar, bg=PALETTE["bg_card"])
        user_frame.pack(side="right", padx=20, pady=12)

        role_badge = "[Doctor]" if self.current_user["role"] == "doctor" else "[Patient]"
        tk.Label(user_frame, text=f"👤 {self.current_user['full_name']} {role_badge}", font=("Segoe UI", 10, "bold"),
                 fg=PALETTE["text_dark"], bg=PALETTE["bg_card"]).pack(side="left", padx=10)

        logout_btn = tk.Button(user_frame, text="Sign Out", font=("Segoe UI", 9), bg=PALETTE["bg_card_subtle"],
                               fg=PALETTE["text_dark"], relief="solid", bd=1, cursor="hand2",
                               command=self.show_auth_screen)
        logout_btn.pack(side="left")

        # Main Notebook
        self.notebook = ttk.Notebook(self.container)
        self.notebook.pack(fill="both", expand=True, padx=15, pady=10)

        # Create Tab Frames
        self.tab_ambulance = tk.Frame(self.notebook, bg=PALETTE["bg_main"])
        self.tab_prediction = tk.Frame(self.notebook, bg=PALETTE["bg_main"])
        self.tab_profile = tk.Frame(self.notebook, bg=PALETTE["bg_main"])
        self.tab_chat = tk.Frame(self.notebook, bg=PALETTE["bg_main"])
        self.tab_doctors = tk.Frame(self.notebook, bg=PALETTE["bg_main"])

        self.notebook.add(self.tab_ambulance, text="  🚨 Emergency Ambulance & Maps  ")
        self.notebook.add(self.tab_prediction, text="  🔬 AI Disease Prediction (NumPy)  ")
        self.notebook.add(self.tab_profile, text="  📊 Health Profile & BMI  ")
        self.notebook.add(self.tab_chat, text="  💬 AI Health Chatbot  ")
        self.notebook.add(self.tab_doctors, text="  👨‍⚕️ Doctors & Appointments  ")

        # Populate tabs
        self._build_ambulance_tab()
        self._build_prediction_tab()
        self._build_profile_tab()
        self._build_chatbot_tab()
        self._build_doctors_tab()

    # ──────────────────────────────────────────────────────────────────────────
    # TAB 1: EMERGENCY AMBULANCE SOS & GOOGLE MAPS
    # ──────────────────────────────────────────────────────────────────────────
    def _build_ambulance_tab(self):
        frame = self.tab_ambulance

        # Left Column: Emergency Input Form (Card)
        left_card = tk.Frame(frame, bg=PALETTE["bg_card"], bd=1, relief="solid", highlightbackground=PALETTE["border"])
        left_card.pack(side="left", fill="both", expand=True, padx=(10, 5), pady=10)

        tk.Label(left_card, text="🚨 1-Click Emergency Ambulance Dispatch", font=("Segoe UI", 14, "bold"),
                 fg=PALETTE["danger"], bg=PALETTE["bg_card"]).pack(anchor="w", padx=20, pady=(15, 2))
        tk.Label(left_card, text="Instant SMS alerts, priority email & direct Google Maps navigation for ambulance drivers",
                 font=("Segoe UI", 9), fg=PALETTE["text_muted"], bg=PALETTE["bg_card"]).pack(anchor="w", padx=20, pady=(0, 15))

        # Fields
        name_entry = tk.Entry(left_card, font=("Segoe UI", 10), bg="#F8FAFC", relief="solid", bd=1)
        age_entry = tk.Entry(left_card, font=("Segoe UI", 10), bg="#F8FAFC", relief="solid", bd=1)
        mobile_entry = tk.Entry(left_card, font=("Segoe UI", 10), bg="#F8FAFC", relief="solid", bd=1)
        area_entry = tk.Entry(left_card, font=("Segoe UI", 10), bg="#F8FAFC", relief="solid", bd=1)
        reason_entry = tk.Entry(left_card, font=("Segoe UI", 10), bg="#F8FAFC", relief="solid", bd=1)

        # Pre-fill user data
        name_entry.insert(0, self.current_user["full_name"])
        age_entry.insert(0, str(self.current_user.get("age", 30)))
        mobile_entry.insert(0, str(self.current_user.get("phone", "9876543210")))
        area_entry.insert(0, "MG Road, Indiranagar, Bengaluru, Karnataka")
        reason_entry.insert(0, "Severe Chest Pain and Breathing Difficulty")

        for label_text, widget in [
            ("Patient Full Name:", name_entry),
            ("Patient Age:", age_entry),
            ("Contact Mobile Number (for SMS Alerts):", mobile_entry),
            ("Emergency Area / Landmark / Address:", area_entry),
            ("Emergency Condition / Symptoms:", reason_entry)
        ]:
            lbl = tk.Label(left_card, text=label_text, font=("Segoe UI", 9, "bold"), fg=PALETTE["text_dark"], bg=PALETTE["bg_card"])
            lbl.pack(anchor="w", padx=20, pady=(4, 1))
            widget.pack(fill="x", padx=20, ipady=4, pady=(0, 6))

        # Right Column: Map Link, Live Tracking & Status Box
        right_card = tk.Frame(frame, bg=PALETTE["bg_card"], bd=1, relief="solid", highlightbackground=PALETTE["border"])
        right_card.pack(side="right", fill="both", expand=True, padx=(5, 10), pady=10)

        tk.Label(right_card, text="📍 Live Emergency Dispatch Center", font=("Segoe UI", 14, "bold"),
                 fg=PALETTE["primary_dark"], bg=PALETTE["bg_card"]).pack(anchor="w", padx=20, pady=(15, 2))

        status_box = scrolledtext.ScrolledText(right_card, font=("Consolas", 9), height=14, bg="#F8FAFC", relief="solid", bd=1)
        status_box.pack(fill="both", expand=True, padx=20, pady=10)
        status_box.insert(tk.END, "System Ready.\nEnter emergency patient details on the left and click 'DISPATCH AMBULANCE NOW'.\n")

        def open_google_maps():
            location = area_entry.get().strip()
            if not location:
                messagebox.showwarning("Warning", "Please enter an area or address first.")
                return
            encoded_loc = urllib.parse.quote(location)
            url = f"https://www.google.com/maps/search/?api=1&query={encoded_loc}"
            webbrowser.open(url)
            status_box.insert(tk.END, f"\n[MAPS] Opened Google Maps search for: {location}\n")

        def dispatch_sos():
            patient = name_entry.get().strip()
            age = age_entry.get().strip()
            phone = mobile_entry.get().strip()
            location = area_entry.get().strip()
            reason = reason_entry.get().strip()

            if not all([patient, age, phone, location]):
                messagebox.showerror("Error", "Please fill in Patient Name, Age, Mobile and Area.")
                return

            encoded_loc = urllib.parse.quote(location)
            maps_route_url = f"https://www.google.com/maps/dir/?api=1&destination={encoded_loc}"

            # Save in database
            req_id = db.execute(
                """INSERT INTO ambulance_requests 
                   (user_id, patient_name, patient_age, mobile_number, area_location, emergency_reason, maps_url, status) 
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (self.current_user["id"] if self.current_user["role"] == "patient" else None,
                 patient, int(age) if age.isdigit() else 30, phone, location, reason, maps_route_url, "Dispatched")
            )

            # Send SMS Alert
            sms_ok = sms.send_ambulance_dispatch_sms(
                patient_name=patient,
                patient_age=age,
                mobile_number=phone,
                area_location=location,
                emergency_reason=reason,
                maps_url=maps_route_url
            )

            # Send Priority Email Alert
            email_target = self.current_user.get("email", "patient@example.com")
            mail.send_ambulance_alert_email(
                to_email=email_target,
                patient_name=patient,
                patient_age=age,
                mobile_number=phone,
                area_location=location,
                emergency_reason=reason,
                maps_url=maps_route_url
            )

            # Log status in terminal and GUI
            status_box.insert(tk.END, f"\n{'='*45}\n")
            status_box.insert(tk.END, f"🚨 EMERGENCY AMBULANCE DISPATCHED [Request #{req_id}]\n")
            status_box.insert(tk.END, f"Time        : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            status_box.insert(tk.END, f"Patient     : {patient} (Age: {age})\n")
            status_box.insert(tk.END, f"Mobile SMS  : Sent to {phone}\n")
            status_box.insert(tk.END, f"Email Alert : Sent to {email_target}\n")
            status_box.insert(tk.END, f"Location    : {location}\n")
            status_box.insert(tk.END, f"Ambulance   : AMB-108 (Paramedics En Route, ETA 8-10 Mins)\n")
            status_box.insert(tk.END, f"Google Maps : {maps_route_url}\n")
            status_box.insert(tk.END, f"{'='*45}\n")
            status_box.see(tk.END)

            # Automatically launch Google Maps navigation route in browser
            webbrowser.open(maps_route_url)

            messagebox.showinfo("🚨 AMBULANCE DISPATCHED",
                                f"Ambulance Unit AMB-108 has been dispatched for {patient}!\n\n"
                                f"• SMS Alert sent to {phone}\n"
                                f"• Email Alert sent to {email_target}\n"
                                f"• Google Maps Route opened directly for navigation.")

        # Action Buttons
        btn_sos = tk.Button(left_card, text="🚨 DISPATCH AMBULANCE NOW (1-Click SOS)", font=("Segoe UI", 11, "bold"),
                            bg=PALETTE["danger"], fg="#FFFFFF", activebackground="#991B1B",
                            relief="flat", cursor="hand2", command=dispatch_sos)
        btn_sos.pack(fill="x", padx=20, ipady=8, pady=(10, 5))

        btn_map = tk.Button(right_card, text="🗺️ Open Direct Google Maps Navigation", font=("Segoe UI", 10, "bold"),
                            bg=PALETTE["secondary"], fg="#FFFFFF", activebackground="#1D4ED8",
                            relief="flat", cursor="hand2", command=open_google_maps)
        btn_map.pack(fill="x", padx=20, ipady=6, pady=(5, 15))

    # ──────────────────────────────────────────────────────────────────────────
    # TAB 2: AI DISEASE PREDICTION (NUMPY POWERED)
    # ──────────────────────────────────────────────────────────────────────────
    def _build_prediction_tab(self):
        frame = self.tab_prediction

        # Left Column: Symptoms Checklist
        left_frame = tk.Frame(frame, bg=PALETTE["bg_card"], bd=1, relief="solid", highlightbackground=PALETTE["border"])
        left_frame.pack(side="left", fill="both", expand=True, padx=(10, 5), pady=10)

        tk.Label(left_frame, text="🔬 AI Clinical Symptom Analyzer", font=("Segoe UI", 14, "bold"),
                 fg=PALETTE["primary_dark"], bg=PALETTE["bg_card"]).pack(anchor="w", padx=15, pady=(12, 2))
        tk.Label(left_frame, text="Select active symptoms to run real-time NumPy vectorized inference",
                 font=("Segoe UI", 9), fg=PALETTE["text_muted"], bg=PALETTE["bg_card"]).pack(anchor="w", padx=15, pady=(0, 8))

        # Checkboxes Container with Canvas for scrolling
        canvas = tk.Canvas(left_frame, bg=PALETTE["bg_card"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(left_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=PALETTE["bg_card"])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(xscrollcommand=scrollbar.set)

        canvas.pack(side="top", fill="both", expand=True, padx=15)
        scrollbar.pack(side="right", fill="y")

        # Clinical Symptoms List
        all_symptoms = [
            ("fever", "High Fever"),
            ("cough", "Persistent Cough"),
            ("headache", "Severe Headache"),
            ("fatigue", "Extreme Fatigue / Weakness"),
            ("nausea", "Nausea & Vomiting"),
            ("chest_pain", "Chest Pain / Tightness (Danger)"),
            ("shortness_of_breath", "Shortness of Breath (Danger)"),
            ("joint_pain", "Joint & Muscle Pain"),
            ("sore_throat", "Sore Throat"),
            ("loss_of_taste", "Loss of Taste / Smell"),
            ("chills", "Shivering Chills"),
            ("sweating", "Excessive Sweating"),
            ("diarrhea", "Diarrhea / Stomach Cramps"),
            ("skin_rash", "Skin Rash / Itching"),
            ("dizziness", "Dizziness & Lightheadedness")
        ]

        self.symptom_vars = {}
        for code, label in all_symptoms:
            var = tk.IntVar(value=0)
            self.symptom_vars[code] = var
            cb = tk.Checkbutton(scrollable_frame, text=label, variable=var, font=("Segoe UI", 10),
                                bg=PALETTE["bg_card"], fg=PALETTE["text_dark"], activebackground=PALETTE["bg_card"],
                                selectcolor=PALETTE["primary_light"])
            cb.pack(anchor="w", pady=2)

        # Duration & Mobile Number controls on left
        extra_box = tk.Frame(left_frame, bg=PALETTE["bg_card_subtle"], bd=1, relief="solid", highlightbackground=PALETTE["border"])
        extra_box.pack(fill="x", padx=15, pady=(10, 5))

        tk.Label(extra_box, text="⏱️ Symptom Duration:", font=("Segoe UI", 9, "bold"), bg=PALETTE["bg_card_subtle"], fg=PALETTE["text_dark"]).pack(anchor="w", padx=10, pady=(6, 2))
        duration_var = tk.StringVar(value="24 hours (1 Day)")
        duration_combo = ttk.Combobox(extra_box, textvariable=duration_var, state="readonly", font=("Segoe UI", 9),
                                      values=["Less than 24 hours", "24 hours (1 Day)", "24–48 hours (1–2 Days)", "3–5 days", "1–2 weeks", "More than 2 weeks"])
        duration_combo.pack(fill="x", padx=10, pady=(0, 6))

        tk.Label(extra_box, text="📱 Mobile Number for Instant Alert:", font=("Segoe UI", 9, "bold"), bg=PALETTE["bg_card_subtle"], fg=PALETTE["text_dark"]).pack(anchor="w", padx=10, pady=(2, 2))
        mobile_pred_entry = tk.Entry(extra_box, font=("Segoe UI", 10), bg="#FFFFFF", relief="solid", bd=1)
        mobile_pred_entry.pack(fill="x", padx=10, ipady=3, pady=(0, 8))
        if self.current_user and self.current_user.get("phone"):
            mobile_pred_entry.insert(0, self.current_user["phone"])
        else:
            mobile_pred_entry.insert(0, "9876543210")

        # Right Column: Prediction Results & Recommendations
        right_frame = tk.Frame(frame, bg=PALETTE["bg_card"], bd=1, relief="solid", highlightbackground=PALETTE["border"])
        right_frame.pack(side="right", fill="both", expand=True, padx=(5, 10), pady=10)

        tk.Label(right_frame, text="📊 Clinical AI Diagnosis & Tablet Instructions", font=("Segoe UI", 14, "bold"),
                 fg=PALETTE["primary_dark"], bg=PALETTE["bg_card"]).pack(anchor="w", padx=15, pady=(12, 2))

        res_box = scrolledtext.ScrolledText(right_frame, font=("Segoe UI", 10), bg="#F8FAFC", relief="solid", bd=1)
        res_box.pack(fill="both", expand=True, padx=15, pady=10)
        res_box.insert(tk.END, "Select symptoms on the left and click 'Run AI Disease Prediction'.\n")

        # Bottom Action buttons frame for WhatsApp / SMS
        action_btn_frame = tk.Frame(right_frame, bg=PALETTE["bg_card"])
        action_btn_frame.pack(fill="x", padx=15, pady=(0, 10))

        last_alert_msg = {"text": "", "phone": ""}

        def open_whatsapp_alert():
            if not last_alert_msg["text"]:
                messagebox.showwarning("Warning", "Please run AI prediction first.")
                return
            wa_url = sms.generate_whatsapp_url(last_alert_msg["phone"], last_alert_msg["text"])
            webbrowser.open(wa_url)

        def open_sms_alert():
            if not last_alert_msg["text"]:
                messagebox.showwarning("Warning", "Please run AI prediction first.")
                return
            sms_url = sms.generate_native_sms_url(last_alert_msg["phone"], last_alert_msg["text"])
            webbrowser.open(sms_url)

        btn_wa = tk.Button(action_btn_frame, text="💬 Share via WhatsApp", font=("Segoe UI", 9, "bold"),
                           bg="#25D366", fg="#FFFFFF", relief="flat", cursor="hand2", command=open_whatsapp_alert)
        btn_wa.pack(side="left", fill="x", expand=True, padx=(0, 5), ipady=5)

        btn_sms_native = tk.Button(action_btn_frame, text="📱 Open in SMS App", font=("Segoe UI", 9, "bold"),
                                   bg=PALETTE["secondary"], fg="#FFFFFF", relief="flat", cursor="hand2", command=open_sms_alert)
        btn_sms_native.pack(side="right", fill="x", expand=True, padx=(5, 0), ipady=5)

        def run_prediction():
            # Extract features into a NumPy array
            symptom_feature_names = ml.SYMPTOM_COLUMNS
            feature_vector = np.zeros(len(symptom_feature_names), dtype=np.int32)

            selected_count = 0
            for i, col in enumerate(symptom_feature_names):
                if col in self.symptom_vars and self.symptom_vars[col].get() == 1:
                    feature_vector[i] = 1
                    selected_count += 1

            if selected_count == 0:
                messagebox.showwarning("Warning", "Please select at least 1 symptom.")
                return

            # Reshape using NumPy for model inference
            input_array = feature_vector.reshape(1, -1)

            # Predict using model
            model = ml.load_model()
            if model is None:
                messagebox.showerror("Error", "Could not load AI disease model.")
                return

            disease = model.predict(input_array)[0]
            proba = model.predict_proba(input_array)[0]
            confidence = float(np.max(proba)) * 100

            # Get tailored precautions, diet, lifestyle, tablets
            precautions = rec.get_precautions(disease)
            lifestyle = rec.get_lifestyle(disease)
            foods_eat = rec.get_food_recommendation(disease)
            foods_avoid = rec.get_foods_to_avoid(disease)
            tablets = rec.get_tablets(disease)

            # Risk / Danger assessment
            is_danger = (
                disease in ["Heart Disease", "Pneumonia", "COVID-19", "Malaria", "Dengue", "Typhoid", "Hypertension"] or
                (self.symptom_vars.get("chest_pain") and self.symptom_vars["chest_pain"].get() == 1) or
                (self.symptom_vars.get("shortness_of_breath") and self.symptom_vars["shortness_of_breath"].get() == 1)
            )

            mobile = mobile_pred_entry.get().strip()

            # Save in database
            pred_id = db.execute(
                """INSERT INTO predictions 
                   (user_id, predicted_disease, confidence, description, precautions, lifestyle, foods_recommended, foods_to_avoid, tablets)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (self.current_user["id"] if self.current_user and self.current_user["role"] == "patient" else None,
                 disease, confidence, f"Clinical AI Prediction with {confidence:.1f}% confidence",
                 json.dumps(precautions), json.dumps(lifestyle),
                 json.dumps(foods_eat), json.dumps(foods_avoid),
                 json.dumps(tablets))
            )

            # Fetch prescribed doctor details
            doctor = rec.get_prescribing_doctor(disease)
            consult_date = datetime.now().strftime("%d %b %Y, %I:%M %p")

            # Build alert message
            alert_msg = sms.format_prediction_alert_message(
                patient_name=self.current_user["full_name"] if self.current_user else "Patient",
                predicted_disease=disease,
                confidence=confidence,
                precautions=precautions,
                tablets=tablets,
                is_emergency=is_danger,
                report_url=f"http://127.0.0.1:5000/report/{pred_id}",
                doctor_name=doctor["name"],
                doctor_specialty=doctor["specialty"],
                consultation_date=consult_date
            )
            last_alert_msg["text"] = alert_msg
            last_alert_msg["phone"] = mobile

            # Dispatch SMS to mobile
            if mobile:
                sms.send_sms(mobile, alert_msg)
                # Directly launch native WhatsApp application for instant send
                sms.open_native_whatsapp(mobile, alert_msg)

            # Send Email result to user
            if self.current_user and self.current_user.get("email"):
                mail.send_prediction_email(
                    to_email=self.current_user["email"],
                    user_name=self.current_user["full_name"],
                    disease=disease,
                    confidence=confidence,
                    precautions=precautions,
                    lifestyle=lifestyle
                )
                if is_danger:
                    mail.send_health_alert(
                        to_email=self.current_user["email"],
                        user_name=self.current_user["full_name"],
                        alert_message=f"🚨 CRITICAL DANGER ALERT: High risk condition detected for {disease}. Please contact a doctor immediately!"
                    )

            # Format result in GUI
            res_box.delete("1.0", tk.END)
            res_box.insert(tk.END, f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
            res_box.insert(tk.END, f"🏥 OFFICIAL MEDICAL PRESCRIPTION & REPORT\n")
            res_box.insert(tk.END, f"📅 Date: {consult_date}\n")
            res_box.insert(tk.END, f"👨‍⚕️ Prescribed By: {doctor['name']} ({doctor['specialty']})\n")
            res_box.insert(tk.END, f"🏥 Hospital: {doctor['hospital']} (Reg: {doctor['reg_no']})\n")
            res_box.insert(tk.END, f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
            res_box.insert(tk.END, f"🎯 DIAGNOSED CONDITION : {disease.upper()}\n")
            res_box.insert(tk.END, f"📈 AI CONFIDENCE SCORE  : {confidence:.1f}%\n")
            res_box.insert(tk.END, f"⏱️ RECORDED DURATION    : {duration_var.get()}\n")
            res_box.insert(tk.END, f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n")

            if is_danger:
                res_box.insert(tk.END, "🚨 DANGER / HIGH-RISK CONDITION DETECTED! 🚨\n")
                res_box.insert(tk.END, "⚠️ This disease or symptom combination requires urgent medical attention.\n")
                res_box.insert(tk.END, "👉 PLEASE CONTACT A DOCTOR IMMEDIATELY or call emergency 108 / 112!\n\n")

            res_box.insert(tk.END, "🛡️ RECOMMENDED PRECAUTIONS:\n")
            for p in precautions[:5]:
                res_box.insert(tk.END, f"  • {p}\n")

            res_box.insert(tk.END, "\n🌱 LIFESTYLE & EXERCISE PROTOCOL:\n")
            for l in lifestyle[:4]:
                res_box.insert(tk.END, f"  • {l}\n")

            res_box.insert(tk.END, "\n🥗 DIETARY GUIDELINES:\n")
            res_box.insert(tk.END, f"  [+] Recommended Foods : {', '.join(foods_eat[:4])}\n")
            res_box.insert(tk.END, f"  [-] Foods to Avoid    : {', '.join(foods_avoid[:4])}\n")

            if tablets:
                res_box.insert(tk.END, "\n💊 PRESCRIBED MEDICATIONS & HOW TO TAKE THEM (Rx):\n")
                for t in tablets:
                    t_name = t.get("name", "Medication")
                    t_dose = t.get("dosage", "As directed")
                    t_how = t.get("how_to_take", "Take after food with water")
                    t_time = t.get("timing", "After Meals")
                    t_dur = t.get("duration", "3-5 days")
                    res_box.insert(tk.END, f"  • {t_name} ({t.get('type', 'Oral')})\n")
                    res_box.insert(tk.END, f"    - Dosage     : {t_dose}\n")
                    res_box.insert(tk.END, f"    - How to Take: {t_how}\n")
                    res_box.insert(tk.END, f"    - Timing     : {t_time} | Duration: {t_dur}\n")

            res_box.insert(tk.END, f"\n📲 NOTIFICATIONS DISPATCHED DIRECTLY:\n")
            res_box.insert(tk.END, f"  • SMS Alert: Sent to {mobile}\n")
            res_box.insert(tk.END, f"  • WhatsApp Native App: Triggered directly with full prescription\n")
            res_box.insert(tk.END, f"  • Digital Report Link: http://127.0.0.1:5000/report/{pred_id}\n")
            res_box.insert(tk.END, "\n⚠️ MEDICAL DISCLAIMER: AI assisted diagnostic recommendation. Follow attending physician's guidance.\n")

            if is_danger:
                messagebox.showwarning("🚨 DANGER ALERT",
                                       f"CRITICAL HEALTH RISK DETECTED FOR: {disease.upper()}\n\n"
                                       "• High risk condition detected.\n"
                                       "• PLEASE CONTACT A DOCTOR IMMEDIATELY!\n"
                                       f"• SMS & WhatsApp dispatched directly to {mobile}")
            else:
                messagebox.showinfo("✅ Analysis Complete",
                                    f"Diagnosis: {disease} ({confidence:.1f}% confidence)\n\n"
                                    f"• Attending Doctor: {doctor['name']}\n"
                                    f"• SMS & WhatsApp dispatched directly to {mobile}\n"
                                    f"• Full prescription generated.")

        btn_predict = tk.Button(left_frame, text="⚡ Run AI Disease Prediction (NumPy)", font=("Segoe UI", 11, "bold"),
                                bg=PALETTE["primary"], fg="#FFFFFF", activebackground=PALETTE["primary_dark"],
                                relief="flat", cursor="hand2", command=run_prediction)
        btn_predict.pack(fill="x", padx=15, ipady=8, pady=10)

    # ──────────────────────────────────────────────────────────────────────────
    # TAB 3: HEALTH PROFILE & NUMPY BMI CALCULATOR
    # ──────────────────────────────────────────────────────────────────────────
    def _build_profile_tab(self):
        frame = self.tab_profile

        card = tk.Frame(frame, bg=PALETTE["bg_card"], bd=1, relief="solid", highlightbackground=PALETTE["border"])
        card.pack(fill="both", expand=True, padx=20, pady=15)

        tk.Label(card, text="📊 Patient Health Profile & Physiological Vitals", font=("Segoe UI", 15, "bold"),
                 fg=PALETTE["primary_dark"], bg=PALETTE["bg_card"]).pack(anchor="w", padx=25, pady=(15, 2))
        tk.Label(card, text="Accurate NumPy body mass index calculation & vital signs tracking",
                 font=("Segoe UI", 9), fg=PALETTE["text_muted"], bg=PALETTE["bg_card"]).pack(anchor="w", padx=25, pady=(0, 15))

        # Grid for vitals
        grid_frame = tk.Frame(card, bg=PALETTE["bg_card"])
        grid_frame.pack(fill="x", padx=25, pady=5)

        h_entry = tk.Entry(grid_frame, font=("Segoe UI", 10), bg="#F8FAFC", relief="solid", bd=1)
        w_entry = tk.Entry(grid_frame, font=("Segoe UI", 10), bg="#F8FAFC", relief="solid", bd=1)
        bp_entry = tk.Entry(grid_frame, font=("Segoe UI", 10), bg="#F8FAFC", relief="solid", bd=1)
        sugar_entry = tk.Entry(grid_frame, font=("Segoe UI", 10), bg="#F8FAFC", relief="solid", bd=1)
        hr_entry = tk.Entry(grid_frame, font=("Segoe UI", 10), bg="#F8FAFC", relief="solid", bd=1)
        temp_entry = tk.Entry(grid_frame, font=("Segoe UI", 10), bg="#F8FAFC", relief="solid", bd=1)

        # Pre-fill defaults
        h_entry.insert(0, "175")
        w_entry.insert(0, "70")
        bp_entry.insert(0, "120/80")
        sugar_entry.insert(0, "95")
        hr_entry.insert(0, "72")
        temp_entry.insert(0, "98.6")

        vitals = [
            ("Height (cm):", h_entry, 0, 0),
            ("Weight (kg):", w_entry, 0, 1),
            ("Blood Pressure (mmHg):", bp_entry, 1, 0),
            ("Blood Sugar (mg/dL):", sugar_entry, 1, 1),
            ("Heart Rate (bpm):", hr_entry, 2, 0),
            ("Body Temp (°F):", temp_entry, 2, 1)
        ]

        for lbl, widget, r, c in vitals:
            sub = tk.Frame(grid_frame, bg=PALETTE["bg_card"])
            sub.grid(row=r, column=c, padx=15, pady=8, sticky="ew")
            grid_frame.columnconfigure(c, weight=1)
            tk.Label(sub, text=lbl, font=("Segoe UI", 9, "bold"), fg=PALETTE["text_dark"], bg=PALETTE["bg_card"]).pack(anchor="w")
            widget.pack(fill="x", ipady=4, pady=(2, 0))

        # BMI Output Result Box
        bmi_card = tk.Frame(card, bg=PALETTE["bg_card_subtle"], bd=1, relief="solid", highlightbackground=PALETTE["border"])
        bmi_card.pack(fill="x", padx=25, pady=15)

        bmi_label = tk.Label(bmi_card, text="BMI Index: -- | Category: --", font=("Segoe UI", 13, "bold"),
                             fg=PALETTE["primary_dark"], bg=PALETTE["bg_card_subtle"])
        bmi_label.pack(padx=20, pady=15)

        def calculate_bmi():
            try:
                h = float(h_entry.get().strip())
                w = float(w_entry.get().strip())

                # NumPy calculation
                h_m = np.array([h / 100.0])
                w_kg = np.array([w])
                bmi = float(w_kg / (h_m ** 2))

                if bmi < 18.5:
                    cat = "Underweight"
                    color = PALETTE["warning"]
                elif 18.5 <= bmi < 25.0:
                    cat = "Normal / Healthy Weight"
                    color = PALETTE["success"]
                elif 25.0 <= bmi < 30.0:
                    cat = "Overweight"
                    color = PALETTE["warning"]
                else:
                    cat = "Obese"
                    color = PALETTE["danger"]

                bmi_label.config(text=f"BMI Score: {bmi:.2f} kg/m²  |  Health Category: {cat}", fg=color)

                # Save profile to DB if user logged in
                if self.current_user and self.current_user["role"] == "patient":
                    db.execute(
                        """INSERT OR REPLACE INTO health_profiles 
                           (user_id, height, weight, bmi, blood_pressure, blood_sugar, heart_rate, body_temperature)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                        (self.current_user["id"], h, w, round(bmi, 2), bp_entry.get().strip(),
                         float(sugar_entry.get().strip()), int(hr_entry.get().strip()), float(temp_entry.get().strip()))
                    )
                    messagebox.showinfo("Profile Updated", f"Vitals saved! Your BMI is {bmi:.1f} ({cat}).")

            except Exception as e:
                messagebox.showerror("Invalid Input", f"Please check numerical values for height and weight: {e}")

        btn_calc = tk.Button(card, text="💾 Calculate BMI & Save Health Vitals", font=("Segoe UI", 11, "bold"),
                             bg=PALETTE["primary"], fg="#FFFFFF", activebackground=PALETTE["primary_dark"],
                             relief="flat", cursor="hand2", command=calculate_bmi)
        btn_calc.pack(padx=25, ipady=8, pady=(5, 15))

    # ──────────────────────────────────────────────────────────────────────────
    # TAB 4: AI HEALTH CHATBOT
    # ──────────────────────────────────────────────────────────────────────────
    def _build_chatbot_tab(self):
        frame = self.tab_chat

        card = tk.Frame(frame, bg=PALETTE["bg_card"], bd=1, relief="solid", highlightbackground=PALETTE["border"])
        card.pack(fill="both", expand=True, padx=20, pady=15)

        tk.Label(card, text="💬 24/7 AI Medical Assistant & Wellness Chat", font=("Segoe UI", 14, "bold"),
                 fg=PALETTE["primary_dark"], bg=PALETTE["bg_card"]).pack(anchor="w", padx=20, pady=(12, 2))

        chat_history = scrolledtext.ScrolledText(card, font=("Segoe UI", 10), bg="#F8FAFC", relief="solid", bd=1)
        chat_history.pack(fill="both", expand=True, padx=20, pady=10)
        chat_history.insert(tk.END, "🤖 AI Assistant: Hello! I am your AI Health Assistant. Tell me what symptoms or health concerns you have today.\n\n")

        msg_frame = tk.Frame(card, bg=PALETTE["bg_card"])
        msg_frame.pack(fill="x", padx=20, pady=(0, 15))

        user_input = tk.Entry(msg_frame, font=("Segoe UI", 11), bg="#F8FAFC", relief="solid", bd=1)
        user_input.pack(side="left", fill="x", expand=True, ipady=6, padx=(0, 10))

        def send_chat():
            txt = user_input.get().strip()
            if not txt:
                return
            chat_history.insert(tk.END, f"👤 You: {txt}\n")
            user_input.delete(0, tk.END)

            # Get AI response
            reply = ai_bot.get_chatbot_response(txt)
            chat_history.insert(tk.END, f"🤖 AI Assistant: {reply}\n\n")
            chat_history.see(tk.END)

        user_input.bind("<Return>", lambda e: send_chat())

        btn_send = tk.Button(msg_frame, text="Send Message", font=("Segoe UI", 10, "bold"),
                             bg=PALETTE["primary"], fg="#FFFFFF", activebackground=PALETTE["primary_dark"],
                             relief="flat", cursor="hand2", command=send_chat)
        btn_send.pack(side="right", ipady=6, padx=(5, 0))

    # ──────────────────────────────────────────────────────────────────────────
    # TAB 5: DOCTORS & APPOINTMENTS
    # ──────────────────────────────────────────────────────────────────────────
    def _build_doctors_tab(self):
        frame = self.tab_doctors

        card = tk.Frame(frame, bg=PALETTE["bg_card"], bd=1, relief="solid", highlightbackground=PALETTE["border"])
        card.pack(fill="both", expand=True, padx=20, pady=15)

        tk.Label(card, text="👨‍⚕️ Certified Medical Specialists & Appointment Booking", font=("Segoe UI", 14, "bold"),
                 fg=PALETTE["primary_dark"], bg=PALETTE["bg_card"]).pack(anchor="w", padx=20, pady=(12, 2))

        # Doctors List Table
        cols = ("Name", "Specialization", "Experience", "Availability", "Email")
        tree = ttk.Treeview(card, columns=cols, show="headings", height=8)
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, anchor="w", width=160)
        tree.pack(fill="both", expand=True, padx=20, pady=10)

        # Load doctors from DB
        doctors = db.query_all("SELECT * FROM doctors")
        for doc in doctors:
            tree.insert("", tk.END, values=(doc["name"], doc["specialization"], f"{doc['experience']} years", doc["availability"], doc["email"]))

        # Appointment Booking Sub-frame
        book_frame = tk.Frame(card, bg=PALETTE["bg_card_subtle"], bd=1, relief="solid", highlightbackground=PALETTE["border"])
        book_frame.pack(fill="x", padx=20, pady=(0, 15))

        tk.Label(book_frame, text="📅 Book an Appointment", font=("Segoe UI", 11, "bold"),
                 fg=PALETTE["text_dark"], bg=PALETTE["bg_card_subtle"]).pack(anchor="w", padx=15, pady=(8, 4))

        bf_inner = tk.Frame(book_frame, bg=PALETTE["bg_card_subtle"])
        bf_inner.pack(fill="x", padx=15, pady=(0, 10))

        date_entry = tk.Entry(bf_inner, font=("Segoe UI", 10), bg="#FFFFFF", relief="solid", bd=1)
        time_entry = tk.Entry(bf_inner, font=("Segoe UI", 10), bg="#FFFFFF", relief="solid", bd=1)
        reason_entry = tk.Entry(bf_inner, font=("Segoe UI", 10), bg="#FFFFFF", relief="solid", bd=1)

        date_entry.insert(0, "2026-09-01")
        time_entry.insert(0, "10:30 AM")
        reason_entry.insert(0, "General Health Consultation")

        for lbl, widget in [("Date (YYYY-MM-DD):", date_entry), ("Time:", time_entry), ("Reason:", reason_entry)]:
            sub = tk.Frame(bf_inner, bg=PALETTE["bg_card_subtle"])
            sub.pack(side="left", padx=5, fill="x", expand=True)
            tk.Label(sub, text=lbl, font=("Segoe UI", 9, "bold"), fg=PALETTE["text_dark"], bg=PALETTE["bg_card_subtle"]).pack(anchor="w")
            widget.pack(fill="x", ipady=3)

        def book_appointment():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Select Doctor", "Please select a doctor from the list above first.")
                return

            item = tree.item(selected[0])
            doc_name = item["values"][0]
            doc_email = item["values"][4]
            doc_row = db.query_one("SELECT id FROM doctors WHERE email = ?", (doc_email,))
            doc_id = doc_row["id"] if doc_row else 1

            d_val = date_entry.get().strip()
            t_val = time_entry.get().strip()
            r_val = reason_entry.get().strip()

            db.execute(
                """INSERT INTO appointments (patient_id, doctor_id, appointment_date, appointment_time, reason, status)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (self.current_user["id"] if self.current_user["role"] == "patient" else 1,
                 doc_id, d_val, t_val, r_val, "Confirmed")
            )

            # Send confirmation email
            mail.send_appointment_confirmation(
                to_email=self.current_user.get("email", "patient@example.com"),
                patient_name=self.current_user["full_name"],
                doctor_name=doc_name,
                appt_date=d_val,
                appt_time=t_val,
                reason=r_val
            )

            messagebox.showinfo("Appointment Confirmed",
                                f"Appointment booked with {doc_name} on {d_val} at {t_val}!\nConfirmation email sent.")

        btn_book = tk.Button(book_frame, text="Confirm Appointment Booking", font=("Segoe UI", 10, "bold"),
                             bg=PALETTE["primary"], fg="#FFFFFF", activebackground=PALETTE["primary_dark"],
                             relief="flat", cursor="hand2", command=book_appointment)
        btn_book.pack(anchor="e", padx=15, pady=(0, 10))


if __name__ == "__main__":
    app = AIHealthAssistantDesktop()
    app.mainloop()

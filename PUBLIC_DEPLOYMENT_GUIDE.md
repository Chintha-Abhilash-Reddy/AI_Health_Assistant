# 🏥 AI Health Assistant — Public Deployment & PWA Guide

**Intelligent Disease Prediction, Health Recommendations, Doctor Consultations, and 24/7 AI Chatbot**

---

## 📋 Quick Navigation

- [Features](#-features)
- [Quick Start (5 minutes)](#-quick-start-5-minutes)
- [Local Development](#-local-development-setup)
- [Public Internet Access](#-public-internet-access)
- [PWA Installation](#-pwa-progressive-web-app)
- [QR Code & Sharing](#-qr-code--sharing)
- [Deployment to Production](#-production-deployment)
- [Testing Checklist](#-testing-checklist)
- [Troubleshooting](#-troubleshooting)

---

## 🌟 Features

✅ **AI Disease Prediction** — Machine Learning model analyzes 25+ symptoms  
✅ **Health Recommendations** — Tailored precautions, diet, and lifestyle  
✅ **Doctor Consultation** — Live chat with certified medical professionals  
✅ **Medical History** — Track predictions, appointments, and reports  
✅ **Ambulance SOS** — Emergency response coordination  
✅ **24/7 Chatbot** — AI-powered health advice  
✅ **Progressive Web App** — Install as app on Android/iOS/Desktop  
✅ **Offline Support** — Limited functionality when offline  
✅ **Public Access** — Share via QR code, link, or web share  
✅ **Responsive Design** — Works on all screen sizes  

---

## ⚡ Quick Start (5 minutes)

### Step 1: Open in VS Code

```bash
# Clone or navigate to your project folder
cd "C:\Users\chint\OneDrive\Desktop\Python\AI_Health_Assistant"

# Open in VS Code
code .
```

### Step 2: Create Virtual Environment & Install Dependencies

Open VS Code Terminal (`Ctrl + `` ` `)  and run:

**Windows (PowerShell/CMD):**
```powershell
# Create virtual environment
python -m venv .venv

# Activate it
.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Initialize database
python -c "import database as db; db.init_db()"

# Train ML model (first time only)
python model_training.py
```

### Step 3: Run Locally

```powershell
python app.py
```

**Output:**
```
🏥 AI HEALTH ASSISTANT — PUBLIC & LOCAL NETWORK ACCESS
===============================================
👉 Local Machine URL : http://127.0.0.1:5000
👉 Local Network URL : http://192.168.x.x:5000 (same Wi-Fi)
👉 Public Access URL : http://0.0.0.0:5000
===============================================
```

### Step 4: Open in Browser

- **Local machine:** http://127.0.0.1:5000
- **From another device on same Wi-Fi:** http://192.168.x.x:5000
- **Public access:** See below ⬇️

---

## 📱 Local Development Setup

### Prerequisites

- Windows 10/11 or macOS/Linux
- Python 3.8+
- VS Code (or any Python IDE)
- pip (Python package manager)

### Full Setup Instructions

#### 1. Clone/Open Project

```bash
cd "C:\Users\chint\OneDrive\Desktop\Python\AI_Health_Assistant"
code .
```

#### 2. Create Virtual Environment

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1  # For PowerShell
# OR
.venv\Scripts\activate.bat  # For Command Prompt
```

#### 3. Install Requirements

```bash
pip install -r requirements.txt
```

**Or use VS Code task:**
- Press `Ctrl + Shift + B`
- Select "Install Dependencies"

#### 4. Configure Environment Variables

Edit `.env` file:

```ini
SECRET_KEY=your_super_secret_key_change_this
FLASK_ENV=development
DEBUG=True
HOST=0.0.0.0
PORT=5000
PUBLIC_APP_URL=http://127.0.0.1:5000

# Email (set to "true" for console mode, no real emails sent)
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
EMAIL_DEV_MODE=true

# Optional: Uncomment for production
# PUBLIC_APP_URL=https://your-domain.com
```

#### 5. Initialize Database

```bash
python -c "import database as db; db.init_db()"
```

#### 6. Train ML Model

```bash
python model_training.py
```

#### 7. Start Development Server

Using terminal:
```bash
python app.py
```

Or use VS Code debugger:
- Press `F5`
- Select "Flask App (Local)"

### Demo Credentials

**Patient Login:**
- Email: `john@example.com`
- Password: `password123`

**Doctor Portal:**
- Navigate to: http://127.0.0.1:5000/doctor/login
- Email: `dr.anil@healthapp.com`
- Password: `password123`

---

## 🌐 Public Internet Access

### Method 1: ngrok (Best for Development)

ngrok creates a secure public HTTPS tunnel to your local server.

#### Setup ngrok

```powershell
# Install ngrok Python wrapper
pip install pyngrok

# Sign up (free): https://ngrok.com/sign-up
# Get your auth token from: https://dashboard.ngrok.com/auth
```

#### Create `public_tunnel.py`

```python
from pyngrok import ngrok
import subprocess
import os
import time

# Set your ngrok auth token (get from https://dashboard.ngrok.com/auth)
ngrok.set_auth_token("YOUR_NGROK_AUTH_TOKEN")

# Create HTTPS tunnel to local Flask server
try:
    tunnel = ngrok.connect(5000, "http")
    public_url = tunnel.public_url
    
    print("\n" + "="*70)
    print("🌐 PUBLIC URL (ngrok Tunnel)")
    print("="*70)
    print(f"Public HTTPS URL: {public_url}")
    print(f"Valid for: 2 hours (free plan)")
    print("="*70 + "\n")
    
    # Set environment variable for QR code generation
    os.environ["PUBLIC_APP_URL"] = public_url
    
    # Start Flask app
    subprocess.run(["python", "app.py"])
except Exception as e:
    print(f"Error: {e}")
    print("Make sure ngrok is installed: pip install pyngrok")
    print("And you have an auth token from: https://dashboard.ngrok.com/auth")
```

#### Run Public Tunnel

```powershell
python public_tunnel.py
```

**Output:**
```
Public HTTPS URL: https://abc123-456.ngrok.io
```

Now your app is accessible from:
- ✅ Windows laptop (any Wi-Fi)
- ✅ Android phone (mobile data)
- ✅ Different locations
- ✅ Different networks
- ✅ HTTPS secured

### Method 2: Production Deployment

For permanent public access, deploy to a cloud platform:

#### Option A: Render (Recommended)

1. **Create Render Account:** https://render.com
2. **Connect GitHub repository**
3. **Create Web Service:**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
4. **Set Environment Variables:**
   ```
   PUBLIC_APP_URL=https://your-app.onrender.com
   FLASK_ENV=production
   SECRET_KEY=your_secret_key
   ```
5. **Deploy** — Render automatically builds and serves your app
6. **Get Public URL:** `https://your-app.onrender.com`

#### Option B: Railway

1. **Create Railway Account:** https://railway.app
2. **Connect GitHub**
3. **Set build & start commands:**
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn app:app --bind 0.0.0.0:$PORT`
4. **Deploy** — Get instant public HTTPS URL

#### Option C: Heroku (with buildpack)

```bash
# Install Heroku CLI
pip install heroku-cli

# Login
heroku login

# Create app
heroku create your-app-name

# Set config
heroku config:set PUBLIC_APP_URL=https://your-app-name.herokuapp.com

# Deploy
git push heroku main
```

---

## 📲 PWA (Progressive Web App)

### Install on Android

#### Method 1: Chrome Browser (Recommended)

1. Open the public URL in **Google Chrome**
2. Tap **Menu (⋮) → Install app**
3. Tap **Install**
4. App appears on home screen
5. Tap to open offline (cached content available)

#### Method 2: Add to Home Screen

1. Open the public URL
2. Tap **Menu (⋮) → Add to Home screen**
3. Confirm

#### Method 3: From Share Button

1. Tap the **"Share"** button in navigation
2. Tap **"Add to Home screen"**

### Install on iPhone/iPad (Safari)

1. Open public URL in **Safari**
2. Tap **Share ↗️ → Add to Home Screen**
3. Name the app and tap **Add**

### Install on Windows Desktop

1. Open the public URL in **Chrome/Edge**
2. Click **Install** button (top-right)
3. App installed and available in Start menu

### Offline Features

Once installed:
- ✅ App loads without internet
- ✅ Static content cached
- ⚠️ Login/API calls require internet
- ℹ️ Offline message shown when needed

---

## 📱 QR Code & Sharing

### Generate QR Code

#### Automatic (from Share Button)

1. Tap **"Share"** button in navigation
2. QR code displays
3. Scan from another device

#### Manual (Terminal)

```bash
# Set your public URL
$env:PUBLIC_APP_URL="https://your-public-url.com"

# Generate QR code
python -c "
import os
from qrcode import QRCode, constants

url = os.getenv('PUBLIC_APP_URL', 'http://127.0.0.1:5000')
qr = QRCode(version=1, error_correction=constants.ERROR_CORRECT_L, box_size=10, border=2)
qr.add_data(url)
qr.make(fit=True)
qr.make_image().save('qr_code.png')
print(f'QR Code saved to qr_code.png')
print(f'URL: {url}')
"
```

### Scan QR Code

1. **Android:** Open camera → tap link → opens browser → tap Install
2. **iPhone:** Camera app → tap notification → opens Safari → Add to Home Screen
3. **Desktop:** Use phone camera or QR code reader app

### Share App

- **Copy link** from Share button
- **Email** share link to contacts
- **WhatsApp/Messages** paste link
- **Web Share API** auto-shares to available apps (Android)

---

## ✅ Testing Checklist

### Local Testing (http://127.0.0.1:5000)

- [ ] Home page loads
- [ ] CSS styling applied
- [ ] Navigation menu works
- [ ] Register functionality works
- [ ] Login functionality works
- [ ] Logout functionality works
- [ ] Dashboard displays
- [ ] Symptom prediction works
- [ ] Doctor list loads
- [ ] Appointment booking works
- [ ] Chat with doctors works
- [ ] AI chatbot responds
- [ ] Ambulance SOS works
- [ ] Medical history displays
- [ ] User profile updates
- [ ] Database saves data
- [ ] Email notifications (dev mode) show in console
- [ ] No console errors (F12 → Console)
- [ ] No network errors (F12 → Network)
- [ ] Responsive on mobile browser (F12 → Device mode)

### Network Testing (http://192.168.x.x:5000)

- [ ] Open from another device on same Wi-Fi
- [ ] All features work
- [ ] Notifications work
- [ ] No connection errors

### Public Testing (https://your-public-url.com)

- [ ] HTTPS works (padlock icon ✅)
- [ ] From different Wi-Fi network
- [ ] From mobile data
- [ ] All features work
- [ ] No localhost/127.0.0.1 errors
- [ ] No CORS errors
- [ ] QR code works
- [ ] Share button works
- [ ] Install button shows (Chrome/Edge)
- [ ] App installs on Android
- [ ] Installed app opens correctly

### PWA Testing

- [ ] Service Worker registered (F12 → Application → Service Workers)
- [ ] Manifest loaded (F12 → Application → Manifest)
- [ ] Offline page shows when disconnected
- [ ] Static assets cached
- [ ] App works offline (limited features)
- [ ] Install prompt shows on first visit
- [ ] Install to home screen works
- [ ] App launches from home screen
- [ ] App runs in standalone mode (no browser UI)
- [ ] Responsive on all screen sizes

### Performance Testing

- [ ] Page loads in < 3 seconds
- [ ] Prediction generates in < 5 seconds
- [ ] No memory leaks (F12 → Performance)
- [ ] Images optimized
- [ ] CSS/JS minified
- [ ] No unused code blocks

### Security Testing

- [ ] No sensitive data in localStorage
- [ ] No API keys in frontend code
- [ ] Passwords hashed in database
- [ ] Sessions valid only for login
- [ ] CSRF protection on forms
- [ ] SQL injection prevented
- [ ] XSS prevention in templates
- [ ] No hardcoded secrets in .env.example

### Browser Compatibility

- [ ] Chrome desktop
- [ ] Chrome mobile
- [ ] Firefox desktop
- [ ] Firefox mobile
- [ ] Safari (macOS)
- [ ] Safari (iOS)
- [ ] Edge (Windows)
- [ ] Samsung Internet (Android)

---

## 🔧 Troubleshooting

### "ModuleNotFoundError: No module named 'flask'"

**Solution:**
```powershell
pip install -r requirements.txt
```

### "Address already in use" (Port 5000)

**Solution:**
```powershell
# Find process using port 5000
Get-NetTCPConnection -LocalPort 5000

# Kill process
Stop-Process -Id <PID> -Force

# Or use different port
python app.py --port 8000
```

### Service Worker fails to register

**Solution:**
- Check browser console (F12) for errors
- Ensure service-worker.js path is correct
- Service workers require HTTPS (ngrok provides this)
- Localhost works for development

### CORS errors when calling API

**Solution:**
- Ensure `ALLOWED_ORIGINS` includes your public URL
- Update `.env`:
  ```
  ALLOWED_ORIGINS=http://localhost:5000,https://your-public-url.com
  ```
- Restart server

### QR code contains localhost instead of public URL

**Solution:**
- Set `PUBLIC_APP_URL` in `.env`
- Restart server
- Clear browser cache (Ctrl+Shift+Delete)
- Regenerate QR code

### App doesn't install on Android

**Solution:**
- Use HTTPS (ngrok or production deployment)
- Check manifest.webmanifest loads (F12 → Application)
- Wait 2-3 seconds after loading
- Install button should appear in address bar or menu
- Chrome needs at least 192x192 icon

### Offline page doesn't show

**Solution:**
- Create `templates/offline.html` with offline message
- Update service-worker.js to serve it
- Or clear all caches (F12 → Application → Storage → Clear All)

### ngrok tunnel expires

**Solution:**
- Free plan: tunnels last 2 hours
- Get new tunnel: run `python public_tunnel.py` again
- For permanent URL: upgrade ngrok or use production deployment

### Database errors

**Solution:**
```powershell
# Reinitialize database
python -c "import database as db; db.init_db()"

# Check health.db exists
dir health.db
```

### ML model not found

**Solution:**
```powershell
python model_training.py
```

### Email not sending

**Solution:**
- Check EMAIL_DEV_MODE=true (emails print to console)
- For real emails: set EMAIL_DEV_MODE=false and add Gmail credentials
- Use Gmail App Password (not regular password)
- Enable 2-Step Verification on Gmail account

---

## 📚 Project Structure

```
AI_Health_Assistant/
├── .vscode/
│   ├── launch.json          # VS Code debug config
│   ├── tasks.json          # VS Code build tasks
│   └── settings.json       # VS Code settings
│
├── app.py                  # Flask main application
├── database.py             # SQLite database setup
├── chatbot.py              # AI chatbot logic
├── email_service.py        # Email notifications
├── sms_service.py          # SMS/WhatsApp integration
├── recommendation.py       # Health recommendations
├── model_training.py       # ML model training
├── test_app.py            # Unit tests
│
├── static/
│   ├── css/
│   │   └── style.css      # Custom styles
│   ├── js/
│   │   ├── script.js      # Global JS
│   │   ├── chatbot.js     # Chatbot logic
│   │   └── doctor_chat.js # Doctor chat logic
│   ├── images/            # Icons & images
│   └── uploads/           # Medical reports
│
├── templates/             # HTML templates
│   ├── base.html         # Base layout (PWA enabled)
│   ├── index.html        # Home page
│   ├── login.html        # Login
│   ├── register.html     # Registration
│   ├── dashboard.html    # User dashboard
│   ├── symptoms.html     # Symptom checker
│   ├── prediction.html   # Prediction results
│   ├── doctors.html      # Doctor directory
│   ├── chatbot.html      # AI chatbot
│   └── ... (more templates)
│
├── data/
│   ├── disease_symptoms.csv
│   └── disease_description.csv
│
├── manifest.webmanifest   # PWA manifest
├── service-worker.js      # Service worker (offline support)
├── requirements.txt       # Python dependencies
├── .env                  # Environment variables (secret)
├── .env.example          # Environment template
├── .gitignore           # Git ignore file
├── README.md            # This file
└── health.db            # SQLite database
```

---

## 🚀 Deployment Checklist

Before going to production:

- [ ] Update SECRET_KEY in .env
- [ ] Set FLASK_ENV=production
- [ ] Disable DEBUG mode
- [ ] Set PUBLIC_APP_URL to real domain
- [ ] Configure MAIL_USERNAME/MAIL_PASSWORD
- [ ] Test all features on production URL
- [ ] Set up SSL certificate (HTTPS)
- [ ] Configure backup strategy
- [ ] Set up monitoring & logging
- [ ] Create privacy policy page
- [ ] Add terms of service
- [ ] Test on all platforms (desktop, tablet, mobile)
- [ ] Verify no sensitive data in logs
- [ ] Set up error tracking (e.g., Sentry)

---

## 📞 Support

### Common Issues

**Q: How do I change the public URL after deployment?**
A: Update `PUBLIC_APP_URL` in `.env` and restart the server. All QR codes will update automatically.

**Q: Can I use the app offline?**
A: Yes! PWA caches static content. Login & API calls require internet. Offline message shows when unavailable.

**Q: How do I uninstall the PWA?**
A: Like any app—press & hold icon → Uninstall (Android) or Remove from Home Screen (iOS).

**Q: Is my data secure?**
A: Yes—passwords are hashed, sessions are secure, HTTPS encrypts data in transit. Never share your SECRET_KEY.

---

## 📝 Medical Disclaimer

⚠️ **IMPORTANT:** AI predictions provided by this application are for informational and educational purposes only. They do NOT constitute a clinical medical diagnosis. Always consult a licensed medical professional for personal health concerns.

---

## 📄 License

This project is provided as-is for educational purposes.

---

## 🎉 You're Ready!

Your AI Health Assistant is now:
- ✅ Running locally
- ✅ Accessible from other devices on the network
- ✅ Available publicly via ngrok or production deployment
- ✅ Installable as a PWA on Android/iOS/Desktop
- ✅ Shareable via QR code
- ✅ Offline-capable
- ✅ Production-ready

**Next Steps:**

1. Customize the app with your branding
2. Add real email credentials for notifications
3. Deploy to production (Render, Railway, etc.)
4. Share the public URL with users
5. Monitor and improve based on feedback

---

**Built with ❤️ using Python, Flask, Bootstrap, AI/ML**

Happy coding! 🚀

# Production Deployment & Hosting Guide

This guide shows how to deploy your **AI Health Assistant** backend & web app to a permanent public HTTPS URL on cloud providers (Render, Railway, Fly.io, Docker, or AWS/DigitalOcean).

---

## 🌟 Method 1: Render.com (Recommended Free/Low Cost 1-Click Setup)

Render provides automatic HTTPS SSL certificates, Git auto-deployment, and environment variable management.

1. **Push your code to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "feat: production AI Health Assistant ready"
   git remote add origin https://github.com/YOUR_USERNAME/ai-health-assistant.git
   git push -u origin main
   ```
2. **Create Web Service on Render**:
   - Go to [dashboard.render.com](https://dashboard.render.com) → Click **New +** → **Web Service**.
   - Connect your GitHub repository.
   - Set:
     - **Runtime**: `Python`
     - **Build Command**: `pip install -r requirements.txt gunicorn`
     - **Start Command**: `gunicorn app:app --workers 4 --threads 2 --timeout 120`
3. **Set Environment Variables in Render Dashboard**:
   - `FLASK_ENV`: `production`
   - `SECRET_KEY`: *(Generate a secure random key)*
   - `PUBLIC_WEB_URL`: `https://ai-health-assistant.onrender.com` *(or your custom domain)*
   - `API_BASE_URL`: `https://ai-health-assistant.onrender.com`
   - `ALLOWED_ORIGINS`: `*`
   - `EMAIL_DEV_MODE`: `true`
4. Click **Deploy Web Service**. Render will build and launch your application at:
   `https://ai-health-assistant.onrender.com`

---

## 🚂 Method 2: Railway.app

1. Go to [railway.app](https://railway.app) → **New Project** → **Deploy from GitHub repo**.
2. Railway automatically detects `Procfile` and `requirements.txt`.
3. Add environment variables in the **Variables** tab (`PUBLIC_WEB_URL`, `API_BASE_URL`, `FLASK_ENV=production`).
4. Under **Settings** → **Domains**, click **Generate Domain** or add your Custom Domain.

---

## 🐳 Method 3: Self-Hosted Docker / VPS (Ubuntu / Debian / AWS EC2)

1. Clone repo onto your server.
2. Run with Docker Compose:
   ```bash
   docker-compose up -d --build
   ```
3. Point Nginx reverse proxy with Certbot SSL:
   ```nginx
   server {
       server_name app.yourdomain.com;

       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```
4. Obtain free SSL certificate:
   ```bash
   sudo certbot --nginx -d app.yourdomain.com
   ```

---

## 🔄 Updating Store URLs After Google & Apple Publish

Once your app is approved on the stores:
1. Copy your public Google Play Store URL and Apple App Store URL.
2. Update the environment variables in your cloud hosting provider:
   - `ANDROID_STORE_URL`: `https://play.google.com/store/apps/details?id=com.health.aiassistant`
   - `IOS_STORE_URL`: `https://apps.apple.com/app/ai-health-assistant/id6739271845`
3. The `/download` page automatically renders updated QR codes pointing directly to the live app stores!

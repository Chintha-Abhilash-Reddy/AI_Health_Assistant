# 📦 PRODUCTION DEPLOYMENT GUIDE

## Overview

This guide covers deploying your AI Health Assistant to production with:
- Public web application (HTTPS)
- Public API backend
- Android app on Google Play Store
- iOS app on Apple App Store

## Part 1: Backend Deployment

### Option A: Deploy on Render.com (Recommended)

1. **Create Render Account**
   - Go to https://render.com
   - Sign up with GitHub

2. **Connect GitHub Repository**
   - Link your GitHub repo
   - Authorize Render

3. **Create Web Service**
   - New → Web Service
   - Select repository
   - Environment: Python 3.11
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app --bind 0.0.0.0:$PORT`

4. **Set Environment Variables**
   ```
   FLASK_ENV=production
   SECRET_KEY=<generate-long-random-string>
   PUBLIC_WEB_URL=https://your-app.onrender.com
   API_BASE_URL=https://your-app.onrender.com
   DATABASE_URL=postgresql://...
   MAIL_USERNAME=<your-email>
   MAIL_PASSWORD=<your-password>
   ```

5. **Deploy**
   - Click Deploy
   - Wait for build and startup
   - Visit https://your-app.onrender.com

### Option B: Deploy on Railway.app

1. **Create Railway Account** → https://railway.app
2. **Connect GitHub**
3. **Create New Project**
4. **Add Service → GitHub Repository**
5. **Configure Build & Start Commands**
   ```
   Build: pip install -r requirements.txt
   Start: gunicorn app:app --bind 0.0.0.0:$PORT
   ```
6. **Set Environment Variables** (same as above)
7. **Deploy** - Railway handles everything

### Option C: Deploy on Heroku (with heroku-cli)

```bash
# Install heroku CLI
npm install -g heroku

# Login
heroku login

# Create app
heroku create your-app-name

# Set environment variables
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=your_secret_key
heroku config:set PUBLIC_WEB_URL=https://your-app-name.herokuapp.com
heroku config:set API_BASE_URL=https://your-app-name.herokuapp.com

# Deploy
git push heroku main
```

## Part 2: Database Configuration

### PostgreSQL Setup (Production)

1. **Create Database**
   - Render: Auto-provisioned with service
   - Railway: Railway PostgreSQL add-on
   - Heroku: Heroku PostgreSQL

2. **Get Connection String**
   - Set as `DATABASE_URL` environment variable
   - Looks like: `postgresql://user:pass@host:5432/dbname`

3. **Initialize Database**
   ```bash
   # From your production server
   python -c "import database as db; db.init_db()"
   ```

## Part 3: Email Configuration

Use transactional email service (NOT Gmail):

### SendGrid (Recommended)

1. Create SendGrid account at https://sendgrid.com
2. Create API key
3. Set environment variables:
   ```
   MAIL_USERNAME=apikey
   MAIL_PASSWORD=SG.xxxxx...
   ```
4. Update `email_service.py` to use SendGrid API

### Alternative Services

- Mailgun: https://mailgun.com
- AWS SES: https://aws.amazon.com/ses/
- Postmark: https://postmarkapp.com
- Brevo (Sendinblue): https://www.brevo.com

## Part 4: Domain Configuration

### Purchase Domain

1. Register domain at:
   - Namecheap.com
   - Google Domains
   - AWS Route53
   - GoDaddy

2. Example domains:
   - aihealth.app
   - healthai.app
   - predictive-health.app

### Configure DNS

**For Render:**
```
CNAME: your-app.onrender.com
```

**For Railway/Heroku:**
```
CNAME: your-app-name.herokuapp.com (or Railway domain)
```

### Enable HTTPS

- Render: Auto-enabled (Let's Encrypt)
- Railway: Auto-enabled (Let's Encrypt)
- Heroku: Auto-enabled (Heroku SSL)

Custom domain HTTPS:
- Most platforms auto-provision SSL

## Part 5: Monitoring & Logging

### Sentry (Error Tracking)

```bash
pip install sentry-sdk
```

Configure in app.py:

```python
import sentry_sdk
sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    traces_sample_rate=1.0
)
```

Set environment variable:
```
SENTRY_DSN=https://your-sentry-dsn@sentry.io/project-id
```

### Logging Setup

Logs are automatically captured by:
- Render: View in dashboard
- Railway: View in logs tab
- Heroku: `heroku logs --tail`

### Uptime Monitoring

Services like:
- Better Stack: https://betterstack.com
- StatusPage: https://www.atlassian.com/software/statuspage
- Pingdom: https://www.pingdom.com

## Part 6: SSL/TLS Certificates

Most platforms provide free SSL:
- Let's Encrypt (auto-renewal)
- Provided by platform

**Verify HTTPS:**
```bash
curl -I https://your-api-domain.com
# Should show "HTTP/2 200" or similar
```

## Part 7: API Configuration for Mobile Apps

Update `capacitor.config.json`:

```json
{
  "server": {
    "url": "https://www.aihealth.app",
    "cleartext": []
  }
}
```

Update mobile app API base URL:

**Android:** `android/app/src/main/assets/capacitor.config.json`
**iOS:** `ios/App/App/capacitor.config.json`

## Part 8: Environment Configuration

### Production .env Variables

```
FLASK_ENV=production
DEBUG=False
SECRET_KEY=<generate-using-secrets-module>
PUBLIC_WEB_URL=https://www.aihealth.app
API_BASE_URL=https://api.aihealth.app
DATABASE_URL=postgresql://user:pass@host/db
MAIL_USERNAME=apikey
MAIL_PASSWORD=<sendgrid-api-key>
ANDROID_STORE_URL=https://play.google.com/store/apps/details?id=com.aihealth.assistant
IOS_STORE_URL=https://apps.apple.com/app/ai-health-assistant/id6739271845
SENTRY_DSN=https://...@sentry.io/...
```

### Verify Configuration

```bash
python config.py  # Prints current configuration
```

## Part 9: Testing Production Deployment

### Test Web App

```bash
# Visit public URL
https://www.aihealth.app

# Test features
- Register new account
- Login
- Symptom prediction
- Doctor chat
- Download page QR codes
```

### Test API

```bash
# Test API endpoints
curl https://api.aihealth.app/api/chat \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"message": "I have fever"}'
```

### Test from Mobile

```bash
# On Android phone
- Connect to different Wi-Fi
- Mobile data
- Navigate to https://www.aihealth.app

# On iPhone
- Connect to different Wi-Fi
- Mobile data
- Safari: https://www.aihealth.app
```

### Check No Localhost References

```bash
# Search entire codebase
grep -r "localhost" --include="*.html" --include="*.js" --include="*.py"
grep -r "127.0.0.1" --include="*.html" --include="*.js" --include="*.py"
grep -r "192.168" --include="*.html" --include="*.js" --include="*.py"

# Should return: NO RESULTS
```

## Part 10: Scaling for High Traffic

When your app grows:

1. **Database**
   - Use managed PostgreSQL with auto-scaling
   - Enable connection pooling
   - Regular backups

2. **API Server**
   - Multiple server instances
   - Load balancing (auto-enabled on most platforms)
   - Redis for caching

3. **CDN**
   - Cloudflare: https://www.cloudflare.com
   - AWS CloudFront
   - Serve static content from edge locations

4. **Rate Limiting**
   - Prevent API abuse
   - Use Flask-Limiter

## Part 11: Security Checklist

- [ ] HTTPS enabled (no HTTP)
- [ ] Secrets in environment variables
- [ ] No hardcoded credentials
- [ ] Database backups enabled
- [ ] CORS properly configured
- [ ] Rate limiting enabled
- [ ] SQL injection prevention
- [ ] XSS protection in templates
- [ ] CSRF tokens on forms
- [ ] Security headers configured
- [ ] Sensitive logs disabled
- [ ] Regular security updates

## Part 12: Backup & Disaster Recovery

### Database Backups

- Render: Auto-backups (7-day retention)
- Railway: Manual backups
- Heroku: Automated backups

### Code Backups

- GitHub (primary)
- Regular pushes

### Disaster Recovery Plan

1. Database corruption → Restore from backup
2. Server crash → Platform auto-restarts
3. Code issues → Rollback to previous version

## Troubleshooting Production Issues

### "Application Error" on Production

1. Check logs: Platform dashboard
2. Verify environment variables
3. Verify database connection
4. Restart service

### Database Connection Errors

```
# Check connection string
echo $DATABASE_URL

# Verify database is running
psql $DATABASE_URL -c "SELECT 1"
```

### Email Not Sending

- Verify email service API key
- Check spam folder
- Review email service logs
- Test with: `python -c "from email_service import send_email; send_email(...)"`

### Slow Performance

- Check server logs for errors
- Enable caching
- Optimize database queries
- Use CDN for static files

### Mobile App Can't Connect to API

- Verify API_BASE_URL is public HTTPS
- Check CORS configuration
- Test with: `curl https://api.example.com`
- Verify SSL certificates valid

## Deployment Checklist

- [ ] Database configured and tested
- [ ] Environment variables set
- [ ] Backend deployment successful
- [ ] Public URL accessible
- [ ] HTTPS working
- [ ] Email service configured
- [ ] No hardcoded localhost references
- [ ] Logs accessible
- [ ] Monitoring enabled
- [ ] Backup strategy in place
- [ ] Security checklist complete
- [ ] Mobile apps can connect to API
- [ ] Download page deployed
- [ ] QR codes working
- [ ] Team access configured

---

**Status: Ready for Production** ✅

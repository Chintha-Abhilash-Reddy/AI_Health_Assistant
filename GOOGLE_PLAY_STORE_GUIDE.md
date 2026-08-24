# Google Play Store Release & Publishing Guide

This guide explains how to generate a signed **Android App Bundle (.aab)** and publish **AI Health Assistant** to the Google Play Store.

---

## 📋 Prerequisites
1. **Google Play Console Developer Account** ($25 one-time registration fee at [play.google.com/console](https://play.google.com/console)).
2. **Android Studio** (or Java JDK 17+ with Android SDK tools installed).

---

## 🔑 Step 1: Generate a Secure Release Signing Keystore

Run the following command in PowerShell / Terminal to create your production upload keystore:

```powershell
keytool -genkey -v -keystore release-key.jks -keyalg RSA -keysize 2048 -validity 10000 -alias health-assistant-key
```

You will be prompted for:
- Keystore password
- First and last name (or Organization name)
- Organization unit & city/state/country

> [!CAUTION]
> **Keep your `release-key.jks` and passwords in a safe backup.** If lost, you will not be able to update your existing app on the Google Play Store. Never commit your keystore or password to public GitHub repositories.

---

## 🏗️ Step 2: Build the Production Android App Bundle (.aab)

Navigate to the `AI_Health_Assistant_Android` directory:

```bash
cd AI_Health_Assistant_Android
```

### Option A: Using Android Studio (Recommended UI Method)
1. Open `AI_Health_Assistant_Android` in **Android Studio**.
2. Go to **Build** → **Generate Signed Bundle / APK...**
3. Select **Android App Bundle** and click **Next**.
4. Choose your `release-key.jks` path and enter your keystore password, alias (`health-assistant-key`), and key password.
5. Select **release** build variant and click **Create**.
6. Your production `.aab` file will be generated at:
   `app/release/app-release.aab`

### Option B: Using Gradle Command Line
```powershell
./gradlew bundleRelease
```

---

## 📱 Step 3: Google Play Console Store Listing Setup

1. Log in to [Google Play Console](https://play.google.com/console).
2. Click **Create App**:
   - **App Name**: `AI Health Assistant - Clinical Diagnosis & Emergency SOS`
   - **Default Language**: `English (United States)`
   - **App or Game**: `App`
   - **Free or Paid**: `Free`
3. Fill in the Store Listing metadata (see [STORE_LISTING_METADATA.md](./STORE_LISTING_METADATA.md)).

---

## 🛡️ Step 4: Data Safety Declaration Guidance

When completing the Google Play **Data Safety Questionnaire**, declare the following based on actual application features:

| Category | Collected / Shared | Data Type | Purpose | Ephemeral / Stored |
|---|---|---|---|---|
| **Location** | Yes (Approximate/Precise) | User Location | Emergency 108 Ambulance Dispatch & Finding Nearest Hospitals | Ephemeral during emergency request |
| **Personal Info** | Yes | Name, Email, Phone | Account login, doctor appointment booking notifications | Stored securely in database |
| **Health Info** | Yes | Symptoms, vitals, height/weight | AI disease prediction, BMI calculation, medical history | Stored for user history |
| **Data Encryption** | Yes | All data | Transferred over secure HTTPS encryption | In transit |
| **Account Deletion** | Yes | User Profile | Option for user to request account and history deletion | Available |

---

## 🎯 Step 5: Content Rating & Target Audience
- **Target Age**: 18 and over (Health/Medical category).
- **Content Rating**: Complete the IARC questionnaire (select *Consumer Health / Medical Info*). Medical disclaimer is present.

---

## 🚀 Step 6: Create Production Track & Upload .aab
1. In Play Console menu, go to **Release** → **Production** (or **Closed Testing** for internal testing).
2. Click **Create new release**.
3. Enable **Play App Signing** (Google manages signing keys automatically).
4. Drag and drop your generated `app-release.aab` bundle.
5. Enter Release notes (e.g. *Initial release: AI symptom analysis, emergency 108 ambulance dispatch, health profile tracker, and doctor consultation portal*).
6. Click **Review Release** → **Start rollout to Production**!

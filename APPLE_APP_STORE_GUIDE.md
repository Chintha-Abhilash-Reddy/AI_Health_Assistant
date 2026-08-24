# Apple App Store Release & Publishing Guide

This guide explains how to configure, sign, test with TestFlight, and submit **AI Health Assistant** to the Apple App Store using Xcode on macOS.

---

## 📋 Prerequisites
1. **Apple Developer Program Membership** ($99/year at [developer.apple.com](https://developer.apple.com)).
2. **Mac Computer** running macOS with **Xcode 15+**.

> [!IMPORTANT]
> **Windows vs macOS Note**:
> While developing cross-platform web and Android applications can be completed on Windows/Linux, Apple's toolchain (Xcode, code signing identities, and App Store Connect uploaders) strictly requires macOS. You can transfer the `AI_Health_Assistant_iOS` folder to any Mac or cloud Mac (such as MacInCloud / GitHub Actions) to run Xcode.

---

## 🔑 Step 1: Configure Apple Developer Account & Identifier

1. Log in to [Apple Developer Portal](https://developer.apple.com/account).
2. Go to **Certificates, Identifiers & Profiles** → **Identifiers**.
3. Click the **+** icon to register a new App ID:
   - **Type**: App IDs
   - **Description**: `AI Health Assistant`
   - **Bundle ID**: Explicit → `com.health.aiassistant`
   - **Capabilities**: Enable *Associated Domains* (for Universal Links) if required.
4. Save and register the identifier.

---

## 🖥️ Step 2: Open Project in Xcode & Configure Signing

1. On your Mac, open the `AI_Health_Assistant_iOS` folder in Xcode.
2. In the project navigator, select the root project node **AIHealthAssistant**.
3. Under the **Signing & Capabilities** tab:
   - Check **Automatically manage signing**.
   - Select your **Team** (your Apple Developer Account).
   - Ensure Bundle Identifier matches `com.health.aiassistant`.
   - Xcode will automatically provision the development and distribution signing certificates.

---

## 📦 Step 3: Archive and Upload to App Store Connect

1. In the top device target selector, select **Any iOS Device (arm64)**.
2. Go to the Xcode menu bar: **Product** → **Archive**.
3. Wait for Xcode to compile and build the release binary.
4. When the **Organizer** window opens:
   - Click **Distribute App**.
   - Choose **App Store Connect** → **Upload**.
   - Keep default distribution options (strip Swift symbols, upload symbols for crash reports).
   - Click **Next** → Review signing certificate → Click **Upload**.
5. Once uploaded, the build will appear in App Store Connect within 10-15 minutes after automated processing.

---

## 🧪 Step 4: Test with TestFlight

1. Log in to [App Store Connect](https://appstoreconnect.apple.com).
2. Open your App → Go to the **TestFlight** tab.
3. Click **Internal Testing** (or **External Testing**).
4. Add testers by email address.
5. Testers will receive an invite to install and test the live app on their iPhones using the official TestFlight app!

---

## 📝 Step 5: App Store Listing & Privacy Nutrition Labels

1. On App Store Connect, go to **App Store** tab → **Prepare for Submission**.
2. Paste the metadata from [STORE_LISTING_METADATA.md](./STORE_LISTING_METADATA.md).
3. **App Privacy (Nutrition Labels)**:
   - **Contact Info**: Name, Email, Phone (used for App Functionality).
   - **Health & Fitness**: Health Data / Vitals (used for App Functionality).
   - **Location**: Coarse/Precise Location (used for Emergency Dispatch Functionality).
   - **Data Linked to User**: Yes (associated with user account for saved history).
   - **Tracking**: No (data is not used to track users across other companies' apps/websites).
4. Upload Screenshots (6.7" iPhone 15/16 Pro Max and 6.5" iPhone 11/14 Plus).
5. Click **Submit for Review**!

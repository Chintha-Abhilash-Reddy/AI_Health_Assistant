# 🚀 MOBILE APP SETUP GUIDE

## Prerequisites

- Node.js 16+ and npm
- Android Studio (for Android builds)
- Xcode (for iOS builds on macOS)
- Java Development Kit (JDK) 11+
- Git

## Step 1: Install Capacitor

```bash
cd AI_Health_Assistant
npm init -y
npm install @capacitor/core @capacitor/cli
npx cap init ai-health-assistant com.aihealth.assistant
```

## Step 2: Install Capacitor Plugins

```bash
npm install @capacitor/device @capacitor/network @capacitor/app @capacitor/keyboard @capacitor/status-bar @capacitor-community/app-launcher
```

## Step 3: Copy Web App Files

```bash
# Create www directory for web assets
mkdir -p www

# Copy Flask templates and static files to www/
# (This would be done automatically during build)
```

## Step 4: Build for Android

### 4a. Initialize Android Project

```bash
npx cap add android
```

### 4b. Open in Android Studio

```bash
npx cap open android
```

### 4c. Configure Android App

In `android/app/build.gradle`:

```gradle
android {
    compileSdkVersion 33
    
    defaultConfig {
        applicationId "com.aihealth.assistant"
        minSdkVersion 21
        targetSdkVersion 33
        versionCode 1
        versionName "1.0.0"
        
        // Required for network security
        useLibrary 'android.net.http.HttpsConnection'
    }
}
```

### 4d. Build Release APK/AAB

```bash
# Debug build (for testing)
npx cap run android

# Release build
cd android
./gradlew clean bundleRelease
# Output: app/release/app-release.aab

# Or for APK
./gradlew assembleRelease
# Output: app/release/app-release.apk
```

### 4e. Sign APK/AAB

Create signing keystore:

```bash
keytool -genkey -v -keystore release-key.keystore \
  -keyalg RSA -keysize 2048 -validity 10000 \
  -alias release-key
```

In `android/app/build.gradle`:

```gradle
signingConfigs {
    release {
        keyStore file('../release-key.keystore')
        keyStorePassword 'YOUR_KEYSTORE_PASSWORD'
        keyAlias 'release-key'
        keyPassword 'YOUR_KEY_PASSWORD'
    }
}

buildTypes {
    release {
        signingConfig signingConfigs.release
    }
}
```

## Step 5: Build for iOS

### 5a. Initialize iOS Project

```bash
npx cap add ios
```

### 5b. Open in Xcode

```bash
npx cap open ios
```

### 5c. Configure iOS App

In Xcode, set:

- Bundle Identifier: `com.aihealth.assistant`
- Version: `1.0.0`
- Build: `1`
- Team ID: (your Apple Developer Team ID)

### 5d. Configure Info.plist

Add required keys:

```xml
<key>NSBonjourServices</key>
<array>
  <string>_http._tcp</string>
  <string>_https._tcp</string>
</array>

<key>NSLocalNetworkUsageDescription</key>
<string>App needs access to local network to function properly</string>

<key>NSBonjourServiceTypes</key>
<array>
  <string>_http._tcp</string>
  <string>_https._tcp</string>
</array>
```

### 5e. Build iOS App

```bash
# In Xcode
# Product → Build For → Running
# Product → Archive

# Or via command line
xcodebuild -workspace ios/App/App.xcworkspace \
  -scheme App \
  -configuration Release \
  -archivePath ~/Library/Developer/Xcode/Archives/App.xcarchive \
  archive
```

## Step 6: Configure Production URLs

Update `capacitor.config.json`:

```json
{
  "server": {
    "url": "https://www.aihealth.app",
    "cleartext": []
  }
}
```

Or set via environment variable:

```bash
API_BASE_URL=https://api.aihealth.app npx cap sync
```

## Step 7: Update Configuration

Create `.env` file in root:

```
PUBLIC_WEB_URL=https://www.aihealth.app
API_BASE_URL=https://api.aihealth.app
ANDROID_STORE_URL=https://play.google.com/store/apps/details?id=com.aihealth.assistant
IOS_STORE_URL=https://apps.apple.com/app/ai-health-assistant/id6739271845
```

## Step 8: Testing

### Android Testing

```bash
# Debug on emulator
npx cap run android

# Debug on device
adb devices  # List connected devices
npx cap run android --target=<device-id>
```

### iOS Testing

```bash
# Debug on simulator
npx cap run ios

# Debug on device
# Use Xcode to select device and run
```

## Step 9: Google Play Store Submission

1. Create Google Play Developer account
2. Create new app with package name `com.aihealth.assistant`
3. Add app details (name, description, screenshots, icon)
4. Add content rating questionnaire
5. Configure privacy policy
6. Upload AAB file
7. Configure pricing
8. Review and publish

## Step 10: Apple App Store Submission

1. Create Apple Developer account
2. Request Apple developer team
3. In App Store Connect:
   - Create new app with bundle ID `com.aihealth.assistant`
   - Add app information
   - Add screenshots and preview
   - Add app icon
   - Configure privacy policy
   - Configure rating
4. In Xcode:
   - Select archive
   - Distribute App
   - App Store Connect
   - Automatically manage signing
5. Review and submit

## Troubleshooting

### Android Build Fails

```bash
cd android
./gradlew clean
./gradlew bundleRelease
```

### iOS Build Fails

```bash
cd ios/App
pod install --repo-update
cd ..
xcodebuild clean -workspace App.xcworkspace -scheme App
```

### App Crashes After Install

- Check logs: `adb logcat` (Android) or Xcode console (iOS)
- Verify API_BASE_URL is set correctly
- Check network security configuration
- Verify HTTPS certificates

### Update URLs After Deployment

```bash
# Update capacitor.config.json
# Or set environment variable and rebuild

export API_BASE_URL="https://api.yourdomain.com"
npx cap sync
```

## Version Updates

When releasing new versions:

1. Increment `versionCode` (Android)
2. Increment `versionName` (Android)
3. Increment `Version` in Xcode (iOS)
4. Increment `Build Number` in Xcode (iOS)
5. Rebuild and test
6. Upload new AAB/IPA to stores
7. Submit for review

---

## Final Checklist

- [ ] Capacitor installed and configured
- [ ] Android project builds successfully
- [ ] iOS project builds successfully
- [ ] Production API URL configured
- [ ] Signing certificates created
- [ ] App icons configured
- [ ] Splash screens configured
- [ ] Permissions configured correctly
- [ ] HTTPS enabled
- [ ] No hardcoded localhost in code
- [ ] Google Play store listing created
- [ ] Apple App Store listing created
- [ ] Privacy policy configured
- [ ] Test flight beta testing started
- [ ] Apps submitted to stores
- [ ] Store URLs configured in download page
- [ ] QR codes generated
- [ ] Public download page deployed

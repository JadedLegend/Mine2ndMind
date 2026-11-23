## **🧭 PDA.OK — Full Command Reference for Building & Publishing an Android APK (Expo / EAS CLI)**

### **📦 0. Environment setup**

Make sure Node and npm are installed:

node -v

npm -v

Install Expo CLI & EAS CLI:

npm install -g expo-cli eas-cli

(If you prefer not to modify PATH, prefix all commands with npx, e.g. npx eas-cli build.)

### **🧰 1. Verify and fix project config**

Confirm your Expo configuration file:

type app.json

It should include:

{

"expo": {

"name": "PDA.OK",

"slug": "pda-ok",

"android": {

"package": "com.braynesnax.pdaok",

"versionCode": 1

}

}

}

(Optional) lock your npm version for CI builds:

npm install -g npm@latest

Run the Expo health check:

npx expo-doctor

### **🧱 2. Log in to Expo**

npx eas-cli login

Confirm login:

npx eas-cli whoami

### **⚙️ 3. Link / configure EAS project**

(Do this once per repo.)

npx eas-cli build:configure

Choose:

- **Account:** braynesnax
- **Create a new project
  **
- Platform: Android

If you ever need to view current linkage:

npx eas-cli project:info

### **🧩 4. Configure build type (APK vs AAB)**

Open or create eas.json with one of the following setups.

For **APK**:

{

"cli": { "version": ">= 3.17.1" },

"build": {

"apk": {

"android": { "buildType": "apk" }

}

}

}

For **Play Store AAB**:

{

"cli": { "version": ">= 3.17.1" },

"build": {

"release": {

"android": { "buildType": "app-bundle" }

}

}

}

### **🚀 5. Build your app**

Start build:

npx eas-cli build -p android --profile preview

npx eas-cli build -p android --profile apk

If prompted:

? Generate a new Android Keystore? » Y

View build status:

npx eas-cli build:list --limit 5

When complete, you’ll see:

Artifact: https://expo.dev/artifacts/eas/<long-id>.apk

Download directly:

npx eas-cli build:download --platform android --profile apk

### **🔐 6. Keystore management**

If you let EAS manage it (recommended), back it up:

npx eas-cli credentials --platform android

Select:

Download Keystore

This gives you:

- my-release-key.jks
- Keystore password
- Key alias
- Key password

Keep these safe — you need them for future Play Store updates.

### **📱 7. Test the APK locally**

adb install app-release.apk

or just copy to your phone and tap it to install (enable “Install unknown apps”).

### **🏪 8. Prepare for Google Play release**

Increment your version numbers before every new upload:

\# inside app.json

"version": "1.0.1",

"android": { "versionCode": 2 }

Rebuild:

npx eas-cli build -p android --profile apk

### **🧭 9. Upload to Google Play (manual)**

1. Go to [Google Play Console](https://play.google.com/console).
2. Create a developer account ($25 one-time).
3. Create a new app → platform “Android”.
4. Upload your **APK** or **AAB** from EAS.
5. Fill in:
  - App name, description, category.
  - Screenshots (1080×1920 recommended).
  - Privacy policy link (can host on GitHub Pages or Notion).
  - Content rating questionnaire.
  - Pricing & distribution countries.
6. Choose **Release track**:
  - *Internal testing* (fastest approval)
  - *Closed / Open testing
    *
  - *Production* for public.
7. Click **Review & publish**.

### **🧩 10. Useful maintenance commands**

| Purpose | Command |
| --- | --- |
| View project info | npx eas-cli project:info |
| --- | --- |
| Check latest builds | npx eas-cli build:list --limit 5 |
| --- | --- |
| Re-run last build | npx eas-cli build -p android --profile apk |
| --- | --- |
| Update Expo SDK | npx expo upgrade |
| --- | --- |
| Run your app locally | npx expo start |
| --- | --- |
| Clean project cache | expo start -c |
| --- | --- |
| Reinstall deps | rm -rf node\_modules && npm install |
| --- | --- |
| Recreate lock file | del package-lock.json && npm install |
| --- | --- |

### **🗂️ 11. Folder cleanup for consistency**

Keep only:

new-pda-app/

app.json

eas.json

package.json

package-lock.json

node\_modules/

Delete if you see:

pnpm-lock.yaml

yarn.lock

### **🔁 12. Updating your app (future releases)**

1. Update code & version fields.

Commit changes:  
  
git add .

git commit -m "Release 1.0.1"

git push origin main

Build again:  
  
npx eas-cli build -p android --profile apk

1. Upload the new APK/AAB to Play Console.

### **🧾 13. References**

- Expo Docs: [https://docs.expo.dev/](https://docs.expo.dev/)
- EAS Build Reference: [https://docs.expo.dev/build/introduction/](https://docs.expo.dev/build/introduction/)
- Play Console Help: [https://support.google.com/googleplay/android-developer/](https://support.google.com/googleplay/android-developer/)
- Expo Keystore Mgmt: [https://docs.expo.dev/app-signing/android/](https://docs.expo.dev/app-signing/android/)
- Versioning: [https://docs.expo.dev/build-reference/app-versions/](https://docs.expo.dev/build-reference/app-versions/)
# APK Extract & Install Toolkit for ADB

Built to make it easy to extract APKs directly from the Play Store and sideload split apps onto your Quest 3, or any Android device, securely and efficiently.

This friendly CLI toolkit helps you pull apps from one device (like BlueStacks or an emulator) and install them onto another (like your Quest 3), without relying on third-party sources.

Install a single app or an entire list with one command. Just provide the names, sit back, and let the script:

Extract, Prepare, and Install. All in one go.

## 📑 Table of Contents

- [🌟 Why I Made This](#-why-i-made-this)
- [🧰 Enabling Developer Mode on Your Devices](#-enabling-developer-mode-on-your-devices)
  - [🔹 BlueStacks (Source Device)](#-bluestacks-source-device)
  - [🔹 Meta Quest 3 (Target Device)](#-meta-quest-3-target-device)
- [🚀 How to Use It](#-how-to-use-it)
  - [1. Extract and Install APKs](#1-extract-and-install-apks)
  - [2. Check If an App Is Installed](#2-check-if-an-app-is-installed)
- [🚧 How It Works (For the Curious)](#-how-it-works-for-the-curious)

---

## 🌟 Why I Made This

I made this for myself because I want the peace of mind and security of using apps pulled directly from the official Google Play Store, without relying on any third-party APK sites or middlemen. But you're welcome to use it or extend it for your own workflows.

Extracting and sideloading APKs — especially split APKs — can be a real pain, especially when using emulators like BlueStacks. This tool streamlines that process:

- Manually downloading Android apps with Google Play Store using BlueStacks
- Extracting all split APKs and sideload them onto my Quest 3.
- Bonus: I wanted a reliable CLI interface with good UX — helpful messages, automatic folder creation, and clean adb integration.

---

## 🧰 Enabling Developer Mode on Your Devices

Before using the scripts, make sure both source and target devices have developer mode enabled. I am using BlueStacks as my source device here.

### 🔹 BlueStacks (Source Device)

1. Open BlueStacks and go to **Settings**.
2. Navigate to the **Advanced** tab.
3. Toggle **Android Debug Bridge (ADB)** to **On**.
4. Click **Save changes**.
5. Connect using:
   ```bash
   adb connect localhost:5555
   ```

👉 [BlueStacks ADB Setup Guide](https://support.bluestacks.com/hc/en-us/articles/23925869130381-How-to-enable-Android-Debug-Bridge-on-BlueStacks-5?utm_source=chatgpt.com)

### 🔹 Meta Quest 3 (Target Device)

1. Visit the [Meta Developer Portal](https://developer.oculus.com/manage/organizations/create/) and create an organization.
2. Verify your Meta account (credit card or 2FA).
3. Open the **Meta Quest app** on your phone:
   - Tap **Menu** → **Devices** → Select your headset
   - Tap **Headset Settings** → **Developer Mode**
   - Toggle **Developer Mode** to **On**, then restart your headset

👉 [Quest 3 Developer Mode Guide](https://knowledge.matts-digital.com/en/virtual-reality/meta/meta-quest-3/how-to-enable-developer-mode-on-the-meta-quest-3/?utm_source=chatgpt.com)

---

## 🚀 How to Use It

> 💡 Tip: Run `adb devices` to list available connected devices and get their IDs for use in the commands below.

### 1. Extract and Install APKs

Use `apk-extract-and-install-with-adb.py` to extract APKs from one device and optionally install to another:

```bash
python apk-extract-and-install-with-adb.py \
  --source-device-id <source-device-id> \
  --target-device-id <target-device-id> \
  --install \
  --verbose \
  --partial-app-names <app-name-1 app-name-2 app-name-3>
```

Note: --partial-app-names takes in one or more app names or the output from the compare-apps-across-devices.py like this
  - com.apple.android.music
  - com.calm.android
  - com.openai.chatgpt
  - com.pinterest
  - com.reddit.frontpage

This will:

- Go through the list of apps
- Search for a package containing `app-name`, e.g. `firefox`, on your source device
- Pull all split APKs
- Save them to `~/Documents/APKs/org.mozilla.firefox/`
- Install them to your target device

You’ll be prompted to select a package if multiple matches are found.

### 2. Check If an App Is Installed

Use `check-apk-installed-on-device.py` to check if a device already has an app installed:

```bash
python check-apk-installed-on-device.py \
  --target-device-id <target-device-id> \
  --verbose \
  --print-all \
  --partial-app-name <app-name>
```

### 3. Compare Apps Across Devices

Use `compare-apps-across-devices.py` to compare user-installed apps between two devices and find out what’s missing or extra.

```bash
python compare-apps-across-devices.py \
  --source-device-id <source-device-id> \
  --target-device-id <target-device-id> \
  --verbose
```

This will:

- Help you identify which apps to extract and install to keep both devices in sync
- List apps installed only on the source (e.g., BlueStacks)
- Optionally list apps installed only on the target (e.g., Quest 3) if you specify `--show-extra-apps-on-target`

---

## 🚧 How It Works (For the Curious)

- Uses `adb shell pm list packages` and `adb shell pm path` to find and pull APKs.
- Handles split APKs automatically and installs with `adb install-multiple`.
- Prompts you for package selection if fuzzy matching returns more than one result.
- Logs are clean and color-coded (dim adb commands, colored UX prompts).
- All APKs are saved in `~/Documents/APKs/{package.name}/` by default.

---

PRs and suggestions welcome!

---

MIT No Attribution License · Created with ❤️ by someone who loves their Quest 3 &
ChatGPT!

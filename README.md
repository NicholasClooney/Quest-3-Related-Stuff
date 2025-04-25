# APK Extract & Install Toolkit for ADB

Built to simplify the process of sideloading split APKs from Play Store apps



A friendly CLI toolkit that helps you extract APKs from one Android device (like an emulator or BlueStacks) and install them onto another (like your Meta Quest 3).

---

## 🌟 Why I Made This

Extracting and sideloading APKs — especially split APKs — can be a real pain, especially when using emulators like BlueStacks. This tool streamlines that process:

- I manually download Android apps using BlueStacks and install them through the Play Store interface.
- Then I can cleanly extract all split APKs and sideload them to my Quest 3.
- Bonus: I wanted a reliable CLI interface with good UX — helpful messages, automatic folder creation, and clean adb integration.

I made this for myself because I want the peace of mind and security of using apps pulled directly from the official Google Play Store, without relying on any third-party APK sites or middlemen.

But you're welcome to use it or extend it for your own workflows.

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
  --partial-app-name <app-name>
```

This will:

- Search for a package containing "", e.g. `firefox`, on your source device
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

---

## ⚙️ How It Works (For the Curious)

- Uses `adb shell pm list packages` and `adb shell pm path` to find and pull APKs.
- Handles split APKs automatically and installs with `adb install-multiple`.
- Prompts you for package selection if fuzzy matching returns more than one result.
- Logs are clean and color-coded (dim adb commands, colored UX prompts).
- All APKs are saved in `~/Documents/APKs/{package.name}/` by default.

---

PRs and suggestions welcome!

---

MIT License · Created with ❤️ by someone who loves their Quest 3


# Crossfire Legion Launcher Troubleshooting Guide

![Crossfire Legion Banner](https://cdn.cloudflare.steamstatic.com/steam/apps/1072190/header.jpg)

Welcome to the **Crossfire Legion Launcher Troubleshooting Guide**!  
This guide helps you fix the notorious "speed bug" in Crossfire Legion, making your game playable again. WARNING: RESPECT THE COOLDOWN FOR FAST CHANGE! Redownload English US pack immidiatly if removed.

---

## 🚩 What is this?

This launcher (FLET GUI) assists you in quickly setting the correct Windows regional settings to fix the game's speed bug.  
You can do this manually, but the launcher automates the process for convenience.

---

## 🐞 The Speed Bug Explained

The main issue is a **locale/number-format bug**:  
The Unity engine reads a speed/timestep value using your Windows “current culture” (decimal comma vs dot).  
On German (and other comma) locales, this value gets parsed incorrectly, causing the game to run at maximum speed.

- **Switching to English (US) display language sometimes helps**—but only if it also changes the regional format/decimal symbol.
- Community reports confirm: EN-US regional format fixes it, but just changing display language alone may not.

---

## 🛠️ How to Fix (Manual & Script Methods)

### Script Setup (Recommended)

1. **Install Python (latest version)**
2. **Install requirements:**  
   ```
   pip install -r requirements.txt
   ```
3. **Run the fixer:**  
   - `regional_format_changer.py`  
   - or use `run_app.bat`
   - Precompiled `.exe` available in the [Releases](./Release) section

---

### Manual Setup

1. **Go to:**  
   `Settings → Time & language → Language & region`
2. **Download English (US) Language Pack** (important!)
3. **Change location and regional format** under Region settings to English (United States)
4. **Restart the game and check if the issue is fixed**

#### If the bug persists:

- Try changing the Windows display language to English (US), sign out and in again, and test again.

This changes how numbers are parsed without changing the whole UI language.

---

## 🧩 Other Fixes

If you still experience the speed bug, try adjusting number formatting directly:

- Open **Control Panel → Region → Additional settings… → Numbers**
  - Set **Decimal symbol** to `.`
  - Set **List separator** to `,`
  - Apply/OK

---

If nothing helps, consider running the game on a Linux distribution (such as Pop!_OS) via Steam/Proton as a workaround.

---

## 🔍 Log Files

Game logs are located at:  
```
C:\Users\<YourName>\AppData\LocalLow\Blackbird Interactive\Crossfire Legion\Player.log
```

---

## 💡 Additional Info & Troubleshooting

- The game can be installed on any drive.
- **What made fixing hard:**  
  - No source code, limited Steam/dev support
- **What didn't help:**  
  - Upgrading `unity_player.dll`
  - Changing Vsync or FPS caps (via Nvidia Profile Inspector or Steam launch options)
  - Changing render methods (`-force-d3d11`, `-force-vulkan`, etc.)
- **What helped:**  
  - Steam forums for Crossfire Legion
- **Miscellaneous launch options tested:**  
  ```
  -force-d3d11, -force-d3d12, -force-vulkan, -force-opengl, -force-gfx-st, -fps 60, -maxFrameRate 60
  -force-gfx-direct, -disable-gfx-jobs
  ```
- **Confirmed:**  
  - The bug is not tied to graphics drivers or render methods. However the bug is fixable with the Source Code.

---

## 📸 Screenshots

![Crossfire Legion Gameplay](https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/1072190/ss_b35e0a8f6dfed3b79e2eb80db6668b8fbfa19698.1920x1080.jpg?t=1755775635)
![Crossfire Legion Settings](https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/1072190/ss_6062dfc1c6520c7684cfe43bfd5fa981326c9ebd.1920x1080.jpg?t=1755775635)

---

## 🙏 Thanks

Thanks to the Crossfire Legion community for sharing fixes and troubleshooting tips, feel free to share this shorted guide!

## ☕ Support me, my hard work and future development:
Crypto Wallet Address: `0xfbe3E2337e7bCfC9245f0C2eAeF16597f0Bb2Dc2` (ETH)  
Crypto Wallet Address: `0x4338665CBB7B2485A8855A139b75D5e34AB0DB94` (LTC)

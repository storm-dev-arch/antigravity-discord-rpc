# 🪐 Google Antigravity Discord RPC & Toast Notifier

<p align="center">
  <img src="antigravity_logo.png" alt="Google Antigravity Logo" width="128" height="128" />
</p>

<p align="center">
  <b>Production-grade Discord Rich Presence & Glassmorphism Toast Notifications for Google Antigravity IDE</b>
</p>

<p align="center">
  <a href="https://github.com/storm-dev-arch/antigravity-discord-rpc/releases"><img src="https://img.shields.io/github/v/release/storm-dev-arch/antigravity-discord-rpc?color=blue&style=for-the-badge" alt="Release"></a>
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python Version">
  <img src="https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white" alt="Platform">
  <img src="https://img.shields.io/badge/UI-PyQt6%20Glassmorphism-41CD52?style=for-the-badge&logo=qt&logoColor=white" alt="PyQt6">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License">
</p>

---

## ✨ Features

- **🎮 Dynamic Discord Rich Presence**:
  - Automatically hooks into Discord IPC via `pypresence`.
  - Reads active task titles dynamically from Antigravity's internal SQLite database (`conversation_summaries.db`).
  - Displays custom status text (e.g. `вайбкодит конкретно`).
  - Displays session elapsed timer with custom Google Antigravity brand logo.
  - Automatically pauses presence when Antigravity is closed.

- **🔔 Sleek Glassmorphism Toast Notifications**:
  - Built with **PyQt6** (`WA_TranslucentBackground`, `FramelessWindowHint`).
  - Dark glass design (Raycast / Linear style) with blurred borders and subtle drop shadow.
  - Smooth 320ms cubic slide-in & fade animation.
  - Plays the crisp Steam Deck / Steam Toast chime on completion.
  - Triggers instantly when Antigravity completes turn generation (`RUNNING -> IDLE`).

- **⚡ Stealth & Background Autorun**:
  - Zero terminal windows (launches silently via `pythonw.exe` & VBS wrapper).
  - Built-in single-instance lock to prevent memory leaks or socket conflicts.
  - One-click Windows autorun integration (`HKCU\Run` and Startup folder).

---

## 🛠️ Architecture

```
antigravity-discord-rpc/
├── rpc_service.py        # Core daemon: process watcher, SQLite parser & Discord IPC
├── config.json           # User configuration (Client ID, details, image assets)
├── run_silent.vbs        # Background runner (launches pythonw silently)
├── start.bat             # Quick launch script
├── stop.bat / stop.py    # Clean shutdown script
├── requirements.txt      # Python dependencies
└── notifier/
    ├── toast.py          # PyQt6 frameless slide-in notification window
    ├── chime.wav         # Authentic notification sound
    └── antigravity_logo.png
```

---

## 🚀 Quick Start

### 1. Requirements
- Windows 10 / 11
- Python 3.10+ installed

### 2. Installation
Clone the repository:
```bash
git clone https://github.com/storm-dev-arch/antigravity-discord-rpc.git
cd antigravity-discord-rpc
pip install -r requirements.txt
```

### 3. Configuration (`config.json`)
You can tweak your Discord presence settings in `config.json`:
```json
{
    "client_id": "1558383244892700683",
    "details": "вайбкодит конкретно",
    "show_active_task": true,
    "default_state": "В потоке вайбкодинга",
    "large_image": "196b84f3d12509f4e19c5b34553a1361",
    "large_text": "Google Antigravity IDE",
    "small_image": "antigravity_icon",
    "small_text": "Vibe Coding Mode",
    "check_interval": 3
}
```

### 4. Running
- To run silently in the background: double-click `run_silent.vbs` or `start.bat`.
- To stop the service: run `stop.bat`.

---

## 📦 Windows Autorun Setup

To have the service automatically start with Windows, add a registry string to:
`HKCU\Software\Microsoft\Windows\CurrentVersion\Run`
- **Name**: `AntigravityDiscordRPC`
- **Value**: `wscript.exe "<FULL_PATH_TO>\run_silent.vbs"`

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

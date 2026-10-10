# 🪐 Google Antigravity Discord RPC & Toast Notifier

<p align="center">
  <img src="antigravity_logo.png" alt="Google Antigravity Logo" width="128" height="128" />
</p>

<p align="center">
  <b>Production-grade Discord Rich Presence & Glassmorphism Toast Notifications for Google Antigravity IDE</b><br>
  <i>Продвинутый Discord Rich Presence статус и всплывающие стеклянные уведомления для Google Antigravity</i>
</p>

<p align="center">
  <a href="#russian">🇷🇺 Читать на русском</a> • <a href="#english">🇬🇧 English Readme</a>
</p>

<p align="center">
  <a href="https://github.com/storm-dev-arch/antigravity-discord-rpc/releases"><img src="https://img.shields.io/github/v/release/storm-dev-arch/antigravity-discord-rpc?color=blue&style=for-the-badge" alt="Release"></a>
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python Version">
  <img src="https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white" alt="Platform">
  <img src="https://img.shields.io/badge/UI-PyQt6%20Glassmorphism-41CD52?style=for-the-badge&logo=qt&logoColor=white" alt="PyQt6">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License">
</p>

---

<a name="russian"></a>
## 🇷🇺 Документация на русском

### ✨ Возможности
- **🎮 Живой статус в Discord**:
  - Читает активные названия задач напрямую из локальной базы данных Antigravity (`conversation_summaries.db`).
  - Отображает кастомный статус (например: `вайбкодит конкретно`).
  - Таймер сессии и официальный логотип Google Antigravity.
  - Автоматически очищает присутствие в Discord, если приложение закрыто.
- **🔔 Всплывающие стеклянные уведомления**:
  - Написаны на **PyQt6** с полупрозрачным блюром и плавной анимацией (стиль Raycast / Linear).
  - Воспроизводят кастомный аудио-эффект при окончании ответа ассистента.
  - Аппаратная защита от дублей уведомлений (Debounce lock).
- **⚡ Бесшумная работа и автозапуск**:
  - Никаких открытых окон CMD/терминалов — запуск через `pythonw.exe` и `run_silent.vbs`.
  - Защита от повторного запуска (single-instance watchdog).
  - Интеграция в автозагрузку Windows.

### 🚀 Быстрый старт
```bash
git clone https://github.com/storm-dev-arch/antigravity-discord-rpc.git
cd antigravity-discord-rpc
pip install -r requirements.txt
```

#### Настройка (`config.json`)
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

#### Запуск
- Для бесшумного запуска в фоне: запусти `run_silent.vbs` или `start.bat`.
- Для остановки: запусти `stop.bat`.

---

<a name="english"></a>
## 🇬🇧 English Documentation

### ✨ Features
- **🎮 Dynamic Discord Rich Presence**:
  - Automatically hooks into Discord IPC via `pypresence`.
  - Dynamically reads active task titles from Antigravity's internal SQLite DB (`conversation_summaries.db`).
  - Displays session elapsed timer with custom Google Antigravity brand logo.
- **🔔 Sleek Glassmorphism Toast Notifications**:
  - Built with **PyQt6** (`WA_TranslucentBackground`, `FramelessWindowHint`).
  - Smooth 320ms cubic slide-in & fade animation with custom audio chime.
  - Triggers instantly on turn completion (`RUNNING -> IDLE`).
- **⚡ Stealth & Background Autorun**:
  - Zero terminal windows (launches silently via `pythonw.exe` & VBS wrapper).
  - Built-in single-instance lock to prevent duplicate instances.

### 🚀 Quick Start
```bash
git clone https://github.com/storm-dev-arch/antigravity-discord-rpc.git
cd antigravity-discord-rpc
pip install -r requirements.txt
start.bat
```

---

## 📄 License
Distributed under the MIT License. See `LICENSE` for details.

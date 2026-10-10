"""
Discord Rich Presence for Google Antigravity IDE.
Displays real-time vibe coding activity, current active task, and project status.
Runs silently in background.
"""

import os
import sys
import time
import json
import sqlite3
import logging
import subprocess
from pathlib import Path

import io
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
LOG_FILE = BASE_DIR / "rpc_service.log"
CONFIG_FILE = BASE_DIR / "config.json"

class FlushFileHandler(logging.FileHandler):
    def emit(self, record):
        super().emit(record)
        self.flush()

logger = logging.getLogger()
logger.setLevel(logging.INFO)
fh = FlushFileHandler(str(LOG_FILE), encoding="utf-8")
fh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
logger.addHandler(fh)

# Redirect stdout and stderr if running under pythonw
if sys.stdout is None:
    sys.stdout = io.StringIO()
if sys.stderr is None:
    sys.stderr = io.StringIO()

try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

import psutil
from pypresence import Presence

# Ensure single instance via psutil
_cur_pid = os.getpid()
for _p in psutil.process_iter(['pid', 'name', 'cmdline']):
    try:
        pname = (_p.info['name'] or '').lower()
        if _p.info['pid'] != _cur_pid and pname in ('python.exe', 'pythonw.exe'):
            _cmd = " ".join(_p.info['cmdline'] or [])
            if "rpc_service.py" in _cmd:
                logging.info(f"Another instance already running (PID: {_p.info['pid']}). Exiting.")
                sys.exit(0)
    except Exception:
        pass

DEFAULT_CONFIG = {
    "client_id": "383226320970055681",
    "details": "Жоско вайбкодит",
    "show_active_task": True,
    "default_state": "В потоке вайбкодинга 🚀",
    "large_image": "https://raw.githubusercontent.com/google/material-design-icons/master/png/action/all_inclusive/materialicons/48dp/2x/baseline_all_inclusive_black_48dp.png",
    "large_text": "Google Antigravity IDE",
    "small_image": "vscode",
    "small_text": "Vibe Coding Mode ON ⚡",
    "check_interval": 3,
    "buttons": [
        {"label": "Google Antigravity", "url": "https://deepmind.google"},
        {"label": "Вайбкодинг", "url": "https://en.wikipedia.org/wiki/Vibe_coding"}
    ]
}

def load_config():
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                cfg = json.load(f)
                return {**DEFAULT_CONFIG, **cfg}
        except Exception as e:
            logging.warning(f"Error loading config.json, using defaults: {e}")
    return DEFAULT_CONFIG

def is_antigravity_running() -> bool:
    for proc in psutil.process_iter(['name']):
        try:
            name = proc.info['name']
            if name and 'antigravity' in name.lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return False

def get_latest_task_info():
    """Reads latest task title and execution state from Antigravity SQLite DB."""
    db_path = Path.home() / ".gemini" / "antigravity" / "conversation_summaries.db"
    if not db_path.exists():
        return None, None

    uri = f"file:{db_path.as_posix()}?mode=ro"
    try:
        conn = sqlite3.connect(uri, uri=True, timeout=2.0)
        cur = conn.cursor()
        cur.execute(
            "SELECT title, status, step_count FROM conversation_summaries "
            "ORDER BY last_modified_time DESC LIMIT 1"
        )
        row = cur.fetchone()
        conn.close()
        if row:
            title, status, step_count = row
            return title, status
    except Exception as e:
        logging.debug(f"Failed to read task DB: {e}")
    return None, None

def main():
    logging.info("Antigravity Discord RPC service starting...")
    config = load_config()

    client_id = config.get("client_id", "383226320970055681")
    rpc = None
    connected = False
    session_start_time = None
    last_state = None
    last_task_status = None

    while True:
        try:
            config = load_config()
            interval = max(2, int(config.get("check_interval", 3)))

            ag_active = is_antigravity_running()

            if not ag_active:
                if connected and rpc:
                    try:
                        logging.info("Antigravity closed. Clearing presence...")
                        rpc.clear()
                        rpc.close()
                    except Exception:
                        pass
                    rpc = None
                    connected = False
                    session_start_time = None
                    last_state = None
                time.sleep(interval)
                continue

            # Antigravity is running
            if not connected or rpc is None:
                try:
                    rpc = Presence(client_id)
                    rpc.connect()
                    connected = True
                    if session_start_time is None:
                        session_start_time = int(time.time())
                    logging.info("Connected to Discord RPC successfully.")
                except Exception as e:
                    logging.warning(f"Waiting for Discord connection... ({e})")
                    connected = False
                    rpc = None
                    time.sleep(interval)
                    continue

            # Build presence payload
            title, status = get_latest_task_info()

            # Trigger smooth toast on turn finish (RUNNING -> IDLE transition)
            if last_task_status == "CASCADE_RUN_STATUS_RUNNING" and status == "CASCADE_RUN_STATUS_IDLE":
                logging.info(f"Antigravity finished turn for '{title}'! Spawning toast notification.")
                try:
                    toast_script = Path(__file__).resolve().parent / "notifier" / "toast.py"
                    if not toast_script.exists():
                        toast_script = Path(r"C:\Users\storm\AppData\Local\Programs\antigravity-notifier\toast.py")
                    if toast_script.exists():
                        toast_msg = f"Ответ готов: {title}" if title else "Ответ готов, шеф!"
                        si = subprocess.STARTUPINFO()
                        si.lpDesktop = r"winsta0\default"
                        subprocess.Popen([
                            sys.executable,
                            str(toast_script),
                            "Google Antigravity",
                            toast_msg[:75]
                        ], startupinfo=si)
                except Exception as toast_err:
                    logging.warning(f"Toast trigger error: {toast_err}")

            last_task_status = status

            details_text = config.get("details", "вайбкодит конкретно")
            if config.get("show_active_task", True) and title:
                # Format task state without emojis/stickers
                task_clean = title.strip()
                if len(task_clean) > 90:
                    task_clean = task_clean[:87] + "..."
                state_text = task_clean
            else:
                state_text = config.get("default_state", "В потоке вайбкодинга")

            payload = {
                "state": state_text[:128],
                "details": details_text[:128],
                "large_image": config.get("large_image"),
                "large_text": config.get("large_text", "Google Antigravity IDE")[:128],
                "small_image": config.get("small_image"),
                "small_text": config.get("small_text", "Vibe Coding Mode ON ⚡")[:128],
                "start": session_start_time
            }

            buttons = config.get("buttons")
            if buttons and isinstance(buttons, list) and len(buttons) > 0:
                valid_buttons = []
                for b in buttons[:2]:
                    if isinstance(b, dict) and "label" in b and "url" in b:
                        valid_buttons.append({
                            "label": str(b["label"])[:32],
                            "url": str(b["url"])
                        })
                if valid_buttons:
                    payload["buttons"] = valid_buttons

            # Only update if something changed or every few cycles
            current_state_key = (details_text, state_text)
            if current_state_key != last_state:
                rpc.update(**payload)
                last_state = current_state_key
                logging.info(f"Updated RPC: {details_text} | {state_text}")
            else:
                # Refresh keepalive
                rpc.update(**payload)

        except Exception as err:
            logging.warning(f"RPC cycle exception: {err}")
            # Reset connection state on pipe break
            try:
                if rpc:
                    rpc.close()
            except Exception:
                pass
            rpc = None
            connected = False

        time.sleep(interval)

if __name__ == "__main__":
    try:
        main()
    except BaseException as exc:
        logging.critical(f"Process exiting with: {type(exc).__name__}: {exc}", exc_info=True)

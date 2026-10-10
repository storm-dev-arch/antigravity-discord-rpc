import os
import psutil

current_pid = os.getpid()
stopped = False
for p in psutil.process_iter(['pid', 'cmdline']):
    try:
        cmd = " ".join(p.info['cmdline'] or [])
        if "rpc_service.py" in cmd and p.pid != current_pid:
            p.kill()
            print(f"Остановлен процесс RPC (PID: {p.pid})")
            stopped = True
    except Exception:
        pass

if not stopped:
    print("Процесс Antigravity Discord RPC не был запущен.")

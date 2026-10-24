import json
import os
import signal
import subprocess
import sys
import time
import fcntl
from datetime import datetime
from pathlib import Path
from threading import Event

folder = Path(__file__).resolve().parent
records_folder = folder / "records"
pid_file = folder / "collector.pid"

script = '''
tell application "System Events"
    set frontApp to first application process whose frontmost is true
    set appName to name of frontApp
    try
        set windowTitle to name of front window of frontApp
    on error
        set windowTitle to ""
    end try
    return appName & "|||" & windowTitle
end tell
'''


def save_file(path, text):
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(text, encoding="utf-8")
    temp.replace(path)


def collect():
    result = subprocess.run(["osascript", "-e", script], capture_output=True,
                            text=True, timeout=20, check=True)
    app, title = result.stdout.strip().split("|||", 1)
    now = datetime.now()
    record = {"recorded_at": now.isoformat(sep=" ", timespec="seconds"),
              "app": app, "title": title}

    path = records_folder / (now.strftime("%Y-%m-%d") + ".json")
    records = json.loads(path.read_text(encoding="utf-8")) if path.exists() else []
    records.append(record)
    save_file(path, json.dumps(records, indent=2, ensure_ascii=False))

    days = {path.stem: json.loads(path.read_text(encoding="utf-8"))
            for path in sorted(records_folder.glob("????-??-??.json"))}
    data = {"updated_at": now.isoformat(timespec="seconds"), "days": days}
    save_file(folder / "activities-data.js", "window.ACTIVITY_DATA = " + json.dumps(data) + ";")


def active_pid():
    if not pid_file.exists():
        return None
    try:
        pid = int(pid_file.read_text())
        if pid <= 1:
            return None
        command = subprocess.run(["ps", "-p", str(pid), "-o", "command="],
                                 capture_output=True, text=True).stdout
        if str(folder / "collector.py") in command and "--run" in command:
            return pid
    except (ValueError, OSError):
        return None


def run():
    with (folder / "collector.lock").open("a") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            return
        records_folder.mkdir(exist_ok=True)
        pid_file.write_text(str(os.getpid()))
        stopped = Event()
        signal.signal(signal.SIGTERM, lambda *_: stopped.set())
        signal.signal(signal.SIGINT, lambda *_: stopped.set())
        try:
            while not stopped.is_set():
                started = time.monotonic()
                try:
                    collect()
                except (subprocess.SubprocessError, ValueError, OSError):
                    pass
                stopped.wait(max(0, 300 - (time.monotonic() - started)))
        finally:
            pid_file.unlink(missing_ok=True)


def main():
    command = sys.argv[1] if len(sys.argv) > 1 else "start"
    if command == "--run":
        run()
        return
    pid = active_pid()
    if command == "stop":
        if pid:
            os.kill(pid, signal.SIGTERM)
        print("Stop requested." if pid else "Not running.")
    elif command == "status":
        print("Running." if pid else "Not running.")
    elif command == "start":
        if pid:
            print("Already running.")
            return
        subprocess.Popen([sys.executable, str(folder / "collector.py"), "--run"],
                         stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL, start_new_session=True)
        print("Collector launched. Open daily_activities.html to view activity.")
    else:
        print("Use: bash run.sh [start|stop|status]")


if __name__ == "__main__":
    main()

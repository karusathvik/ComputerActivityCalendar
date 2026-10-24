#!/usr/bin/env python3
import argparse
import fcntl
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import time
from datetime import datetime

ROOT = Path(__file__).resolve().parent
RECORDS = ROOT / "records"
PID = ROOT / "collector.pid"
LOCK = ROOT / "collector.lock"
LOG = ROOT / "collector.log"
INTERVAL = 300

APPLESCRIPT = '''
tell application "System Events"
    set frontApp to first application process whose frontmost is true
    set appName to name of frontApp
    try
        set windowTitle to name of front window of frontApp
    on error errorMessage
        log errorMessage
        set windowTitle to ""
    end try
    return appName & "|||" & windowTitle
end tell
'''


def atomic_write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent,
                                         delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(text)
        temporary.replace(path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def publish():
    days = {}
    for path in sorted(RECORDS.glob("????-??-??.json")):
        days[path.stem] = json.loads(path.read_text(encoding="utf-8"))
    payload = {"updated_at": datetime.now().isoformat(timespec="seconds"), "days": days}
    atomic_write(ROOT / "activities-data.js", "window.ACTIVITY_DATA = " +
                 json.dumps(payload, ensure_ascii=True) + ";\n")


def capture():
    result = subprocess.run(["osascript", "-e", APPLESCRIPT], capture_output=True,
                            text=True, timeout=20)
    if result.stderr.strip():
        print(result.stderr.strip(), file=sys.stderr, flush=True)
    if result.returncode or "|||" not in result.stdout:
        raise RuntimeError(result.stderr.strip() or "No active window returned")
    app, title = result.stdout.strip().split("|||", 1)
    return {"recorded_at": datetime.now().isoformat(sep=" ", timespec="seconds"),
            "app": app, "title": title}


def append_record(record):
    path = RECORDS / (record["recorded_at"][:10] + ".json")
    records = json.loads(path.read_text(encoding="utf-8")) if path.exists() else []
    records.append(record)
    atomic_write(path, json.dumps(records, indent=2, ensure_ascii=False) + "\n")
    publish()


def active_pid():
    try:
        pid = int(PID.read_text().strip())
        if pid <= 1:
            return None
        command = subprocess.run(["ps", "-p", str(pid), "-o", "command="],
                                 capture_output=True, text=True, check=True).stdout
        return pid if str(ROOT / "collector.py") in command and "--run" in command else None
    except (OSError, ValueError, subprocess.SubprocessError):
        return None


def run():
    with LOCK.open("a") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            print("A collector is already running.", flush=True)
            return
        atomic_write(PID, str(os.getpid()))
        running = True

        def stop(signum, frame):
            nonlocal running
            running = False

        signal.signal(signal.SIGTERM, stop)
        signal.signal(signal.SIGINT, stop)
        print("Collector started; sampling every five minutes.", flush=True)
        try:
            publish()
            while running:
                started = time.monotonic()
                try:
                    record = capture()
                    if running:
                        append_record(record)
                        print(record["recorded_at"] + " Recorded activity", flush=True)
                except Exception as error:
                    print("Collection failed: " + str(error), file=sys.stderr, flush=True)
                remaining = max(0, INTERVAL - (time.monotonic() - started))
                deadline = time.monotonic() + remaining
                while running and time.monotonic() < deadline:
                    time.sleep(min(1, max(0, deadline - time.monotonic())))
        finally:
            PID.unlink(missing_ok=True)
            print("Collector stopped.", flush=True)


def main():
    parser = argparse.ArgumentParser(description="Local macOS activity collector")
    parser.add_argument("command", nargs="?", choices=["start", "stop", "status"], default="start")
    parser.add_argument("--run", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()
    if sys.platform != "darwin":
        parser.error("This collector requires macOS.")
    if args.run:
        run()
        return
    pid = active_pid()
    if args.command == "status":
        print(f"Running (PID {pid})." if pid else "Not running.")
    elif args.command == "stop":
        if pid:
            os.kill(pid, signal.SIGTERM)
            print("Stop requested.")
        else:
            print("Not running.")
    elif pid:
        print(f"Already running (PID {pid}).")
    else:
        with LOG.open("a") as log:
            process = subprocess.Popen([sys.executable, str(ROOT / "collector.py"), "--run"],
                                       cwd=ROOT, stdin=subprocess.DEVNULL, stdout=log,
                                       stderr=log, start_new_session=True)
        for _ in range(30):
            if active_pid():
                print("Collecting in the background every five minutes.")
                print("Open the calendar: open daily_activities.html")
                print("Allow macOS Accessibility/Automation permissions if prompted.")
                print("Troubleshooting: tail -f collector.log")
                return
            if process.poll() is not None:
                break
            time.sleep(0.1)
        raise SystemExit("Collector did not start. Check collector.log.")


if __name__ == "__main__":
    main()

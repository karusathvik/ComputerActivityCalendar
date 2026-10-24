import requests
from datetime import datetime
import time
from DesktopAgent.DesktopInfo import  DesktopInfo
tmp = DesktopInfo()

success = True
while success:
    sample_started = time.monotonic()
    res = tmp.sample_frontmost_info_n(1, 1)[0]
    app, title = res["app"], res["title"]
    print("app = ", app)
    print("title = ", title)


    curr_time = datetime.now().isoformat(sep=' ', timespec='seconds')
    data_info = {"record_time":curr_time, "app": app, "title": title}

    try:
        request = requests.post('http://localhost:8080/ComputerActivityCalendar_war/api/records', data=data_info, timeout = 10)
        request.raise_for_status()
        success = "success" in request.json()
    except (requests.RequestException, ValueError) as error:
        print("Upload failed:", error, flush=True)
        success = False
    if success:
        time.sleep(max(0, 300 - (time.monotonic() - sample_started)))




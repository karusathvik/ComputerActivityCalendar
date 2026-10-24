import requests
from datetime import datetime
import time
from DesktopAgent.DesktopInfo import  DesktopInfo
tmp = DesktopInfo()

success = True
while success:
    time.sleep(5)
    res = tmp.sample_frontmost_info_n(1, 1)
    app, title = res[0]["app"], res[0]["title"]
    curr_time = datetime.now().isoformat(sep=' ', timespec='seconds')
    data_info = {"record_time":curr_time, "app": app, "title": title}

    try:
        request = requests.post('http://localhost:8080/ComputerActivityCalendar_war/api/records', data=data_info, timeout = 10)
    except:
        success = False
    success = "success" in request.text




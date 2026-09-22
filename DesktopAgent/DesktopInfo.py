import pyautogui, time, pyautogui, os, sys, subprocess
from PIL import Image 
from AppKit import NSWorkspace


#pil / pyautogui and potentially OCR is for later if
#classification proves to be inefficent 

class DesktopInfo:
    start = 0 
    def __init__(self):
        start = time.time()
    
    def get_frontmost_info(self):
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

        result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
        app, title = result.stdout.strip().split("|||", 1)
        return app, title
    
    def sample_frontmost_info_n(self, n : "int", len = 1):
        '''time would be the custom timer between samples in s'''
        arr = []
        for i in range(n):
            app, title = self.get_frontmost_info()
            arr.append({"app": app, "title": title})
            time.sleep(len)
        return arr
        





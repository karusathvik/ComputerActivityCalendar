import pyautogui as pg #https://pyautogui.readthedocs.io/en/latest/screenshot.html#the-locate-functions
import os, sys
from PIL import Image #https://pillow.readthedocs.io/en/stable/handbook/overview.html
from AppKit import NSWorkspace

'''
im1 = pg.screenshot() #this is a pil object
im1 = im1.convert("L") #convert the image to grayscale 

#have to save the image explicitly for it show 
im1.save("irstimage.png") 
im1.show()
'''
      
#pyobjc allows for python the use of AppKit 

#we are mostly interseted in current screen instead of a split screen so we just care about the frontmost


#https://developer.apple.com/documentation/appkit/nsworkspace
workspace = NSWorkspace.sharedWorkspace() 
arr_of = workspace.runningApplications()
for app in arr_of:
    if (app.isActive):
        ...
        #print(app.localizedName())
        #print(app.bundleIdentifier())
        #print(app.processIdentifier(), '\n')

app = workspace.frontmostApplication()
# https://developer.apple.com/documentation/appkit/nsrunningapplication
#print(app.localizedName())
#print(app.bundleIdentifier())
fm_pid = app.processIdentifier()

#attempting to accesss the viewing window 


'''
    The following below gives access to the name of the active app
    as well as the window that is being show 

    App: Google Chrome
    Window: Python time Module - Google Chrome - Sathvik

    for ex ; this itself gives a big information without an expensive LLM API


'''
import subprocess

def get_frontmost_info():
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


app, title = get_frontmost_info()


import time 

start = time.time()
'''
for i in range(10):
    time.sleep(3)
    app, title = get_frontmost_info()
    print("App:", app)
    print("Window:", title)
'''
 
 #with this, i could just return {"App" : app, "Window" : title} in a json like format 



from DesktopAgent.DesktopInfo import DesktopInfo

tmp = DesktopInfo()
res = tmp.sample_frontmost_info_n(10, 1)
print(res)
# ComputerActivityCalendar
Clone the project in your terminal and run the following commands:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

# Version 1
This version involves running apache tomcat and then the python script that imports apples built in features to get the current active app and tab.
The problem with this was it was just to complex and it did not fit my original vision which was something along the lines of deploying this on the cloud, and then user has to also download a collector app which would just run the python script. Hence version 2, which is just a python script that lives in the bash shell that you can activate. Now the user information is with the user, they can check the code to see that its not invasive and its only purpose is to like really get an outline of what you are doing on a day 2 to basis for ourself and hence version 2.

(This version was a full stack ish application and what this project was trying to achieve is more like v2 since v1 would be too invasive for a normal user).

# Version 2
Just clone the repository and then run the following commands:

```bash
cd ComputerActivityCalendar/script
bash run.sh
open daily_activities.html
```

To start the collector:

```bash
bash run.sh
```

To look at the daily_activities:

```bash
open daily_activities.html
```

To stop the collector:

```bash
bash run.sh stop
```

Note that this version is just running the script and starts a process that runs in the background so you have to make sure you close the processes or it just runs. Additionally, all the information of the user would be stored in script/records as I opted to store the day to day information as json files so that way we can control the data (working with a central sql database would not be applicable here). The collectory.py just runs the oa script, creates process, handles deadlocks / concurrency if accidental threads are stared. Worst case, go to system manager and quit the threads if too many were created.

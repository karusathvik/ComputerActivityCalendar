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

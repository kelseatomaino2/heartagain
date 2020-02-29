# heartagain

### Starting the App - By Kelsea

SSH into pi `ssh pi@172.20.10.4`
Password: `heartagain`

To start background task, `tmux` and to disconnect `Ctrl + b` then to reattach `tmux a` to create a new window `Ctrl %` then to switch between windows `Ctrl ARROW_OF_CHOICE`
Then run `python3 manage.py readSensor`
Start webapp `python3 manage.py runserver 172.20.10.4`

Navigate to link 172.20.10.4:8000/home/
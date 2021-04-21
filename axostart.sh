# script to turn the bot on

nohup python3 main.py > my.log 2>&1 &
echo $! > save_pid.txt


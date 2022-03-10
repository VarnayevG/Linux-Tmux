# Linux-Tmux
Script which runs N isolated Jupyter environments in tmux.
[Task description](https://gitlab.com/fpmi-atp/tpos21/-/blob/master/homeworks/hw-01.md)


Usage:

start:
python3 task1_1.py start --num_users={num_users}
stop:
python3 task1_1.py stop --session_name={session_name} --num={num}
stop_all:
python3 task1_1.py stop_all --session_name='{session_name}'
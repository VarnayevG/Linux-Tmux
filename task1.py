import os
import libtmux
from tqdm import tqdm

def get_port():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 0))
    return s.getsockname()[1]


def get_rnd_str(k=10):
    import random
    import string
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=k))


def start(num_users: int, base_dir: str ='./') -> None:
    server = libtmux.Server()
    session_name = get_rnd_str()
    with open('session_names.txt', 'w+') as f:
        f.write(session_name)
    session = server.new_session(session_name=session_name)
    for user in tqdm(range(num_users)):
        folder = f'user_{user+1}'
        try:
            os.makedirs(os.path.join(base_dir, folder))
            window = session.new_window(window_name=folder,
                                        start_directory=base_dir)
        except FileExistsError:
            window = session.new_window(window_name=folder,
                                        start_directory=base_dir)
        pane = window.attached_pane
        token, port = get_rnd_str(),  get_port()
        pane.send_keys(f'cd user_{user+1}')
        pane.send_keys(f'python3 -m venv env_user_{user+1}')
        pane.send_keys(f'source {user+1}/bin/activate')
        pane.send_keys(f"jupyter notebook --no-browser --port {int(port)} --ip 0.0.0.0 --NotebookApp.token='{token}'")


def stop(session_name: str, num: int) -> None:
    server = libtmux.Server()
    current_session = server.find_where({'session_name': session_name})
    if current_session:
        current_window = f'user_{num}'
        current_session.kill_window(current_window)


def stop_all(session_name: str) -> None:
    server = libtmux.Server()
    server.kill_session(target_session=session_name)


def main():
    import argparse
    parser = argparse.ArgumentParser()
    args = {'cmd': str,
            '--num_users': int,
            '--base_dir': str,
            '--session_name': str,
            '--num': int,
           }
    for k, v in args.items():
        if k == 'cmd':
            parser.add_argument(k, type=v, choices=['start', 'stop', 'stop_all'])
        elif k=='--base_dir':
            parser.add_argument(k, type=v, default='./')
        else:
            parser.add_argument(k, type=v)
    parsed_args = parser.parse_args()
    if parsed_args.cmd == 'start':
        if parsed_args.num_users and parsed_args.base_dir:
            start(parsed_args.num_users, parsed_args.base_dir)
        else:
            parser.error('check arguments')
    elif parsed_args.cmd == 'stop':
        if parsed_args.session_name and parsed_args.num:
            stop(parsed_args.session_name, parsed_args.num)
        else:
            parser.error('check arguments')
    else:
        if parsed_args.session_name:
            stop_all(parsed_args.session_name)
        else:
            parser.error('check arguments')

if __name__ == '__main__':
    main()


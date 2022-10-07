import alt_proc_path
from _import import *
import subprocess
import psutil
import signal
import alt_proc.cfg

def get_pid():
    log = subprocess.check_output('netstat -tupln 2>&1', shell=True)
    for line in log.decode().split('\n'):
        m = re.match(fr'.+0.0.0.0:{port}.+?(\d*)/python.+', line)
        if m:
            return int(m.group(1))

def kill():
    pid = get_pid()
    if pid:
        print('Killing', pid)
        proc = psutil.Process(pid)
        for child in proc.children(recursive=True):
            child.kill()
        proc.kill()
    while True:
        time.sleep(3)
        pid = get_pid()
        if not pid:
            break

def sigterm_handler(_signo, _stack_frame):
    kill()
    print('Exiting')
    sys.exit()

main_dir = os.path.dirname(__file__) + '/'
cfg = alt_proc.cfg.read(f'{main_dir}_cfg/_main.cfg')
port = cfg.port

pid = get_pid()
if pid:
    kill()

print('Starting')
subprocess.Popen(f'{sys.executable} {main_dir}/main.py', shell=True)
for i in range(5):
    time.sleep(1)
    pid = get_pid()
    if pid:
        break

signal.signal(signal.SIGTERM, sigterm_handler)

while True:
    try:
        time.sleep(3)

        pid = get_pid()
        if not pid:
            sys.exit()
    except KeyboardInterrupt:
        kill()


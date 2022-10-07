from _import import *
import alt_proc.pg_async
from _types import User

app = None
main_dir = os.path.dirname(__file__) + '/'
cfg = alt_proc.cfg.read(f'{main_dir}_cfg/_main.cfg')
sputnik_cfg = alt_proc.cfg.read_global('sputnik')

login_last_bad_dt = 0
users = {}
for user in cfg.users:
    users[user.login] = User(**user)

db = alt_proc.pg_async.DB(**cfg.db)




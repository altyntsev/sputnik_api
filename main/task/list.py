import alt_path
from _import import *
from _types import *
import _global

method = alt_proc.file.name(__file__)
path = alt_proc.file.dir(__file__)
path = path[path.find('/main/'):]
router = APIRouter(prefix=path[5:-1])


class Params(Strict):
    pass

class Task(Strict):
    name: str
    descr: str

class Res(Strict):
    tasks: List[Task]


@router.get(
    '/' + method,
    response_model=Res,
    summary='Task list'
)
async def main(login=Depends(auth.get_login)):
    tasks = []
    task_cfg = alt_proc.cfg.read(_global.main_dir + '_cfg/tasks.cfg')
    for name, descr in task_cfg.tasks.items():
        tasks.append(Task(name=name, descr=descr))

    return Res(tasks=tasks)

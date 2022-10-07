import alt_path

import lib
from _import import *
from _types import *
import _global

method = alt_proc.file.name(__file__)
path = alt_proc.file.dir(__file__)
path = path[path.find('/main/'):]
router = APIRouter(prefix=path[5:-1])

class ScriptRes(Strict):
    proc_id: int
    iscript: int
    name: str
    status: Optional[Literal['WAIT', 'NEXT', 'RUN', 'DONE']]
    result: Optional[Literal['SUCCESS', 'FATAL', 'ERRORS']]

class ProcRes(Strict):
    event_id: int
    task_id: int
    ctime: datetime
    task: str = Field(
        ...,
        title='Task name'
    )
    title: str = Field(
        ...,
        title='Event title'
    )
    status: Optional[Literal['WAIT', 'RUN', 'DONE', 'DELETED']]
    result: Optional[Literal['SUCCESS', 'FATAL', 'ERRORS']]
    params: Optional[Any]
    proc_id: Optional[int]
    scripts: Optional[List[ScriptRes]]

class Res(Strict):
    procs: List[ProcRes]


@router.get(
    '/' + method,
    response_model=Res,
    summary='Processing list'
)
async def main(project_id: int, login=Depends(auth.get_login)):
    sql = """
        select event_id from sputnik.procs 
        where project_id=:project_id order by event_id desc limit 30 
        """
    events = await _global.db.query(sql, {'project_id': project_id})

    event_ids = [event['event_id'] for event in events]
    res = await lib.alt_proc_api('post', '/proc/list', {'event_ids': event_ids})
    procs_by_event_id = {proc['event_id']: proc for proc in res['procs']}
    res = await lib.alt_proc_api('post', '/event/list', {'event_ids': event_ids})
    events_by_event_id = {event['event_id']: event for event in res['events']}

    procs = []
    for event_id in event_ids:
        proc = {}
        proc.update(events_by_event_id.get(event_id, {}))
        proc.update(procs_by_event_id.get(event_id, {}))
        procs.append(ProcRes(**proc))

    return Res(procs=procs)

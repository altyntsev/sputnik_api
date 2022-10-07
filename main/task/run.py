import alt_path
import lib
from _import import *
from _types import *
import _global

method = alt_proc.file.name(__file__)
path = alt_proc.file.dir(__file__)
path = path[path.find('/main/'):]
router = APIRouter(prefix=path[5:-1])


class Params(Strict):
    task: str = Field(
        ...,
        title='Task Name'
    )
    title: str = Field(
        ...,
        title='Processing Name'
    )
    project_id: int = Field(
        ...,
        title='Project ID'
    )
    params: Optional[Any] = Field(
        None,
        title='Processing params'
    )


class Res(Strict):
    event_id: int


@router.post(
    '/' + method,
    response_model=Res,
    summary='Run processing'
)
async def main(params: Params = Body(...), login=Depends(auth.get_login)):
    if not params.title:
        lib.fatal('Processing title empty')

    event_params = params.params if params.params else {}
    event_params['project_id'] = params.project_id
    event = {
        'task': params.task,
        'title': params.title,
        'params': event_params
    }

    res = await lib.alt_proc_api('post', '/event/emit', event)

    sql = '''
        insert into sputnik.procs (event_id, project_id) values (:event_id, :project_id)
        '''
    values = {'event_id': res['event_id'], 'project_id': params.project_id}
    await _global.db.insert(sql, values, id_field='project_id')

    return Res(event_id=res['event_id'])

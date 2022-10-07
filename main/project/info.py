import alt_path
from _import import *
from _types import *
import _global

method = alt_proc.file.name(__file__)
path = alt_proc.file.dir(__file__)
path = path[path.find('/main/'):]
router = APIRouter(prefix=path[5:-1])


class Res(Project):
    border_gj: str


@router.get(
    '/' + method,
    response_model=Res,
    summary='Project info'
)
async def main(
        project_id: int = Query(
            ...,
            title='project_id'
        ),
        login=Depends(auth.get_login)):
    sql = f"""
            select *, st_asgeojson(border) as border_gj
            from sputnik.projects
            where project_id=:project_id 
            """

    project: Res = await _global.db.find_one(Res, sql, {'project_id': project_id})

    return project

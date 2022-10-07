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


class Res(Strict):
    projects: List[Project]


@router.get(
    '/' + method,
    response_model=Res,
    summary='Save project',
    # language=YAML
    description='''
        Description: Save project to database
        '''
)
async def main(login=Depends(auth.get_login)):
    sql = f"""
            select *
            from sputnik.projects
            order by project_id 
            """

    projects = await _global.db.find(Project, sql)

    return Res(projects=projects)

import alt_path

import alt_proc.time
import lib
from _import import *
from _types import *
import _global

method = alt_proc.file.name(__file__)
path = alt_proc.file.dir(__file__)
path = path[path.find('/main/'):]
router = APIRouter(prefix=path[5:-1])


class Params(Strict):
    name: str = Field(
        ...,
        title='Project Name'
    )
    start_date: Optional[str] = Field(
        None,
        title='Start date'
    )
    end_date: Optional[str] = Field(
        None,
        title='End date'
    )
    border: str = Field(
        ...,
        title='Region border (GeoJson)'
    )


class Res(Strict):
    project_id: int = Field(
        ...,
        title='project_id'
    )


@router.post(
    '/' + method,
    response_model=Res,
    summary='Save project',
    # language=YAML
    description='''
        Description: Save project to database
        '''
)
async def main(params: Params = Body(...), login=Depends(auth.get_login)):

    sql = '''
        insert into sputnik.projects 
        (login, name, start_date, end_date, border)
        values (:login, :name, :start_date, :end_date, :border)
        '''
    values = params.dict()
    values['login'] = login
    if not params.name:
        lib.fatal('Project Name empty')
    values['border'] = gis.geom.Geom(geojson=params.border).wkt()

    project_id = await _global.db.insert(sql, values, id_field='project_id')

    return Res(project_id=project_id)

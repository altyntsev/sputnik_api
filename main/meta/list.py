from _import import *
from _types import *
import lib
import _global

method = alt_proc.file.name(__file__)
path = alt_proc.file.dir(__file__)
path = path[path.find('/main/'):]
router = APIRouter(prefix=path[5:-1])

class MetaRes(Meta):
    border_gj: str

class Res(Strict):
    metas: List[MetaRes]

@router.get(
    '/' + method,
    response_model=Res,
    summary='Scenes metadata for date'
)
async def main(project_id: int, date: str, login=Depends(auth.get_login)):
    sql = f"""
            select *, st_asgeojson(border) as border_gj from sputnik.meta 
            where project_id=:project_id and date=:date 
            order by date  
            """
    metas = await _global.db.find(MetaRes, sql, {'project_id': project_id, 'date': date})

    return Res(metas=metas)

from _import import *
from _types import *
import lib
import _global

method = alt_proc.file.name(__file__)
path = alt_proc.file.dir(__file__)
path = path[path.find('/main/'):]
router = APIRouter(prefix=path[5:-1])

class Res(Strict):
    dates: List[str]

@router.get(
    '/' + method,
    response_model=Res,
    summary='Date list of available metadata'
)
async def main(project_id: int, login=Depends(auth.get_login)):
    sql = f"""
            select date from sputnik.meta 
            where project_id=:project_id
            group by date
            order by date  
            """
    rows = await _global.db.query(sql, {'project_id': project_id})
    dates = [row['date'] for row in rows]

    return Res(dates=dates)

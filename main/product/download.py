from _import import *
from fastapi.responses import FileResponse
import _global
import lib

method = alt_proc.file.name(__file__)
path = alt_proc.file.dir(__file__)
path = path[path.find('/main/'):]
router = APIRouter(prefix=path[5:-1])

@router.get(
    '/' + method,
    summary='Download product'
)
async def main(project_id: int, product_id: str, login=Depends(auth.get_login)):

    file = f'{_global.sputnik_cfg.storage_dir}projects/{project_id}/rgb/{product_id}.tif'
    if not os.path.exists(file):
        lib.fatal('File not exists')

    return FileResponse(path=file, filename=f'{product_id}.tif', media_type='application/x-binary')

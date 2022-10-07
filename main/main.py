import alt_proc_path
from _import import *
import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
os.environ.pop('PROJ_LIB', None)
from titiler.core.factory import TilerFactory
import _global

import project.new
import project.list
import project.info
import task.list
import task.run
import proc.list
import meta.list
import meta.dates
import product.list
import product.download

app = FastAPI(dependencies=[Depends(auth.get_login)])
_global.app = app

@app.on_event('startup')
async def startup_event():
    await _global.db.connect()

@app.get('/')
async def root():
    return RedirectResponse('/redoc')

@app.get('/exit')
async def exit():
    sys.exit()

app.include_router(project.new.router)
app.include_router(project.list.router)
app.include_router(project.info.router)
app.include_router(task.list.router)
app.include_router(task.run.router)
app.include_router(proc.list.router)
app.include_router(meta.list.router)
app.include_router(meta.dates.router)
app.include_router(product.list.router)
app.include_router(product.download.router)

cog = TilerFactory(router_prefix='cog')
app.include_router(cog.router, prefix='/cog', tags=['Cloud Optimized GeoTIFF'])

app.add_middleware(CORSMiddleware, allow_origins=_global.cfg.cors, allow_credentials=True,
                   allow_methods=['*'], allow_headers=['*'])



@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error = exc.errors()[0]
    msg = error['msg'] + ':' + error['loc'][-1]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({'detail': msg}),
    )


@app.on_event('startup')
async def startup_event():
    await _global.db.connect()


@app.get('/')
async def root():
    return RedirectResponse('/redoc')

app.mount('/storage', StaticFiles(directory=_global.sputnik_cfg.storage_dir + 'projects'))

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=_global.cfg.port,
                reload=True, reload_dirs=[_global.main_dir])

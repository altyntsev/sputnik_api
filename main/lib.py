import alt_path
from _import import *
from osgeo import ogr
import _global
import aiohttp

def fatal(msg):

    print('Fatal:', msg)
    raise HTTPException(status_code=461, detail=msg)

async def alt_proc_api(method, url, params=None):
    api_cfg = _global.cfg.alt_proc_api
    auth = aiohttp.BasicAuth(api_cfg.user, api_cfg.pwd)
    async with aiohttp.ClientSession(auth=auth) as session:
        if method == 'get':
            async with session.get(api_cfg.url + url, params=params) as res:
                if res.status != 200:
                    raise Exception('alt_proc_api failed')
                else:
                    return await res.json()
        else:
            async with session.post(api_cfg.url + url, json=params) as res:
                if res.status != 200:
                    raise Exception('alt_proc_api failed')
                else:
                    return await res.json()





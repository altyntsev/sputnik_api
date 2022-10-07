import asyncio
from aiocogeo import COGReader
from pprint import pprint

# tif_file = '/_geol/wd/sputnik/storage/projects/1/rgb/cog.tif'
tif_file = '/_geol/wd/sputnik/storage/projects/1/rgb/S2A_48UWD_20210102_0_L2A-rgb.tif'
# z, x, y = 8, 203, 83
z, x, y = 13, 6517, 2684

async def tile():
    async with COGReader(tif_file) as cog:
        # tile = await cog.get_tile(x, y, z)
        print(cog.epsg)
        pprint(cog.profile)
        partial_data = await cog.read(bounds=(500000.0, 5800000.0, 600000.0, 5900000.0), shape=(512,512))

loop = asyncio.get_event_loop()
loop.run_until_complete(tile())
loop.close()
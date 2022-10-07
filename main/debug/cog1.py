import asyncio
from rio_tiler.io import COGReader
from pprint import pprint

# tif_file = '/_geol/wd/sputnik/storage/projects/1/rgb/cog.tif'
tif_file = '/_geol/wd/sputnik/storage/projects/1/rgb/S2A_48UWD_20210102_0_L2A-rgb.tif'
# z, x, y = 8, 203, 83
z, x, y = 13, 6517, 2684

with COGReader(tif_file) as cog:
    print(cog.dataset)
    print(cog.tms.identifier)
    print(cog.minzoom)
    print(cog.maxzoom)
    print(cog.bounds)
    print(cog.crs)
    print(cog.geographic_bounds)
    print(cog.colormap)


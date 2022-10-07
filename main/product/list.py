from _import import *
from _types import *
import _global

method = alt_proc.file.name(__file__)
path = alt_proc.file.dir(__file__)
path = path[path.find('/main/'):]
router = APIRouter(prefix=path[5:-1])

class Product(Strict):
    product: str
    product_id: str
    date: str
    meta: Optional[Any]

class Res(Strict):
    products: List[Product]

@router.get(
    '/' + method,
    response_model=Res,
    summary='Scenes metadata for date'
)
async def main(project_id: int, product=None, login=Depends(auth.get_login)):
    where = ['project_id=:project_id']
    values = {'project_id': project_id}
    if product:
        where.append('product=:product')
        values['product'] = product
    sql = f"""
            select product, product_id, date, meta 
            from sputnik.products 
            where {' and '.join(where)} 
            order by date  
            """
    products = await _global.db.find(Product, sql, values)

    return Res(products=products)

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.infra.database import get_session
from app.modules.product.schemas import ProductResponse
from app.modules.product.service import ProductService

router = APIRouter(prefix="/api/v1/products", tags=["产品管理相关接口"])

def get_product_service(session: AsyncSession = Depends(get_session)) ->ProductService:
        return ProductService(session)

@router.get("", response_model=list[ProductResponse])
async def list_product(
        category:str | None = None,
        service: ProductService = Depends(get_product_service)
) -> list[ProductResponse]:
        return await service.list_product(category)
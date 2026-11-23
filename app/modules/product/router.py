from decimal import Decimal
from typing import Annotated
from fastapi import APIRouter, Depends, Query, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.infra.database import get_session
from app.modules.product.schemas import ProductResponse
from app.modules.product.service import ProductService

router = APIRouter(prefix="/api/v1/products", tags=["产品管理相关接口"])

MAX_PRODUCT_ID = 2**63 - 1

def get_product_service(session: AsyncSession = Depends(get_session)) ->ProductService:
        return ProductService(session)

# 根据商品类型查询有效的商品
@router.get("", response_model=list[ProductResponse])
async def list_product(
        category:str | None = None,
        service: ProductService = Depends(get_product_service)
) -> list[ProductResponse]:
        return await service.list_product(category)

# 多险种推荐候选产品查询接口
@router.get("/candidates", response_model=list[ProductResponse])
async def list_candidates(
        categories: list[str] = Query(min_length=1),
        premium_min: Decimal | None = None,
        limit_per_category: int = Query(default=5, ge=0),
        service: ProductService = Depends(get_product_service)
) -> list[ProductResponse]:
        return await service.list_candidates(categories, premium_min, limit_per_category)

# 根据产品 ID 查询产品详情
@router.get("/{id}", response_model=ProductResponse)
async def get_product_by_id(
        id: Annotated[int, Path(alias="id", ge=1, le=MAX_PRODUCT_ID)],
        service: ProductService = Depends(get_product_service)
) -> ProductResponse:
        product = await service.get_product_by_id(id)
        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="该产品不存在"
            )
        return product
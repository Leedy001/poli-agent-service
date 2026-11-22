from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Product


class ProductRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

# 根据category查询有效的保险
    async def query_by_category(self, category: str | None = None) -> list[Product]:

        conditions = [Product.status == 'active']
        if category:
            conditions.append(Product.category == category)

        result = await self.session.scalars(
            select(Product)
            .where(*conditions)
        )

        return result.all()

# 按险种和保费条件查询可用于推荐的候选保险产品
    async def find_limited_by_category(
            self,
            category: str,
            premium_min: Decimal | None,
            limit: int,
    ) -> list[Product]:
        conditions = [
            Product.status == 'active',
            Product.category == category
        ]
        if premium_min is not None:
            conditions.append(Product.min_premium < premium_min)
        products = await self.session.scalars(
            select(Product)
            .where(*conditions)
            .order_by(
                Product.min_premium.asc().nullslast(),
                Product.id.desc()
            )
            .limit(limit)
        )
        return products.all()

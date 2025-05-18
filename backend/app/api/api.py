from fastapi import APIRouter
from .endpoints import auth, users, customers, products, quotations, invoices, settings

api_router = APIRouter()

# 認証関連のエンドポイント
api_router.include_router(auth.router, prefix="/auth", tags=["認証"])

# ユーザー関連のエンドポイント
api_router.include_router(users.router, prefix="/users", tags=["ユーザー"])

# 顧客関連のエンドポイント
api_router.include_router(customers.router, prefix="/customers", tags=["顧客"])

# 商品関連のエンドポイント
api_router.include_router(products.router, prefix="/products", tags=["商品"])

# 見積書関連のエンドポイント
api_router.include_router(quotations.router, prefix="/quotations", tags=["見積書"])

# 請求書関連のエンドポイント
api_router.include_router(invoices.router, prefix="/invoices", tags=["請求書"])

# システム設定関連のエンドポイント
api_router.include_router(settings.router, prefix="/settings", tags=["システム設定"]) 
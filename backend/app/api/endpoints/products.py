from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ... import crud, models, schemas
from ...database import get_db
from ...auth import get_current_active_user

router = APIRouter()

@router.get("/", response_model=List[schemas.Product])
def read_products(
    skip: int = 0,
    limit: int = 100,
    sort_by: str = "created_at",
    sort_order: str = "desc",
    category: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """
    商品一覧を取得します。
    """
    products = crud.get_products(
        db,
        skip=skip,
        limit=limit,
        sort_by=sort_by,
        sort_order=sort_order,
        category=category,
        status=status,
    )
    return products

@router.post("/", response_model=schemas.Product)
def create_product(
    product: schemas.ProductCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """
    新しい商品を作成します。
    """
    db_product = crud.get_product_by_code(db, product_code=product.product_code)
    if db_product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product code already registered",
        )
    return crud.create_product(db=db, product=product, user_id=current_user.id)

@router.get("/{product_id}", response_model=schemas.Product)
def read_product(
    product_id: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """
    指定されたIDの商品情報を取得します。
    """
    db_product = crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    return db_product

@router.put("/{product_id}", response_model=schemas.Product)
def update_product(
    product_id: str,
    product: schemas.ProductUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """
    指定されたIDの商品情報を更新します。
    """
    db_product = crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    if product.product_code and product.product_code != db_product.product_code:
        existing_product = crud.get_product_by_code(db, product_code=product.product_code)
        if existing_product:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product code already registered",
            )
    return crud.update_product(
        db=db,
        product_id=product_id,
        product=product,
        user_id=current_user.id,
    ) 
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ... import crud, models, schemas
from ...database import get_db
from ...auth import get_current_active_user

router = APIRouter()

@router.get("/", response_model=List[schemas.Customer])
def read_customers(
    skip: int = 0,
    limit: int = 100,
    sort_by: str = "created_at",
    sort_order: str = "desc",
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """
    顧客一覧を取得します。
    """
    customers = crud.get_customers(
        db,
        skip=skip,
        limit=limit,
        sort_by=sort_by,
        sort_order=sort_order,
        status=status,
    )
    return customers

@router.post("/", response_model=schemas.Customer)
def create_customer(
    customer: schemas.CustomerCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """
    新しい顧客を作成します。
    """
    return crud.create_customer(db=db, customer=customer, user_id=current_user.id)

@router.get("/{customer_id}", response_model=schemas.Customer)
def read_customer(
    customer_id: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """
    指定されたIDの顧客情報を取得します。
    """
    db_customer = crud.get_customer(db, customer_id=customer_id)
    if db_customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )
    return db_customer

@router.put("/{customer_id}", response_model=schemas.Customer)
def update_customer(
    customer_id: str,
    customer: schemas.CustomerUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """
    指定されたIDの顧客情報を更新します。
    """
    db_customer = crud.get_customer(db, customer_id=customer_id)
    if db_customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )
    return crud.update_customer(
        db=db,
        customer_id=customer_id,
        customer=customer,
        user_id=current_user.id,
    ) 
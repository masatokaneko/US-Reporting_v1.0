from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ... import crud, models, schemas
from ...database import get_db
from ...auth import get_current_active_user

router = APIRouter()

@router.get("/", response_model=List[schemas.Quotation])
def read_quotations(
    skip: int = 0,
    limit: int = 100,
    sort_by: str = "created_at",
    sort_order: str = "desc",
    status: Optional[str] = None,
    customer_id: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """
    見積書一覧を取得します。
    """
    quotations = crud.get_quotations(
        db,
        skip=skip,
        limit=limit,
        sort_by=sort_by,
        sort_order=sort_order,
        status=status,
        customer_id=customer_id,
    )
    return quotations

@router.post("/", response_model=schemas.Quotation)
def create_quotation(
    quotation: schemas.QuotationCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """
    新しい見積書を作成します。
    見積書作成権限が必要です。
    """
    if not current_user.create_quote_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    return crud.create_quotation(db=db, quotation=quotation, user_id=current_user.id)

@router.get("/{quotation_id}", response_model=schemas.Quotation)
def read_quotation(
    quotation_id: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """
    指定されたIDの見積書情報を取得します。
    """
    db_quotation = crud.get_quotation(db, quotation_id=quotation_id)
    if db_quotation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quotation not found",
        )
    return db_quotation

@router.put("/{quotation_id}", response_model=schemas.Quotation)
def update_quotation(
    quotation_id: str,
    quotation: schemas.QuotationUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """
    指定されたIDの見積書情報を更新します。
    見積書作成権限が必要です。
    """
    if not current_user.create_quote_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    db_quotation = crud.get_quotation(db, quotation_id=quotation_id)
    if db_quotation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quotation not found",
        )
    if db_quotation.status != "draft":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only update draft quotations",
        )
    return crud.update_quotation(
        db=db,
        quotation_id=quotation_id,
        quotation=quotation,
        user_id=current_user.id,
    )

@router.post("/{quotation_id}/request-approval", response_model=schemas.Quotation)
def request_quotation_approval(
    quotation_id: str,
    approver_id: str,
    notes: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """
    指定されたIDの見積書を承認依頼します。
    見積書作成権限が必要です。
    """
    if not current_user.create_quote_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    db_quotation = crud.get_quotation(db, quotation_id=quotation_id)
    if db_quotation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quotation not found",
        )
    if db_quotation.status != "draft":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only request approval for draft quotations",
        )
    return crud.request_quotation_approval(
        db=db,
        quotation_id=quotation_id,
        approver_id=approver_id,
        notes=notes,
    )

@router.post("/{quotation_id}/approve", response_model=schemas.Quotation)
def approve_quotation(
    quotation_id: str,
    notes: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """
    指定されたIDの見積書を承認します。
    見積書承認権限が必要です。
    """
    if not current_user.approve_quote_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    db_quotation = crud.get_quotation(db, quotation_id=quotation_id)
    if db_quotation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quotation not found",
        )
    if db_quotation.status != "pending_approval":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only approve pending quotations",
        )
    return crud.approve_quotation(
        db=db,
        quotation_id=quotation_id,
        approver_id=current_user.id,
        notes=notes,
    ) 
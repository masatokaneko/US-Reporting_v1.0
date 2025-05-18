from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ... import crud, models, schemas
from ...database import get_db
from ...auth import get_current_active_user

router = APIRouter()

@router.get("/", response_model=List[schemas.Invoice])
def read_invoices(
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
    請求書一覧を取得します。
    """
    invoices = crud.get_invoices(
        db,
        skip=skip,
        limit=limit,
        sort_by=sort_by,
        sort_order=sort_order,
        status=status,
        customer_id=customer_id,
    )
    return invoices

@router.post("/", response_model=schemas.Invoice)
def create_invoice(
    invoice: schemas.InvoiceCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """
    新しい請求書を作成します。
    請求書作成権限が必要です。
    """
    if not current_user.create_invoice_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    return crud.create_invoice(db=db, invoice=invoice, user_id=current_user.id)

@router.get("/{invoice_id}", response_model=schemas.Invoice)
def read_invoice(
    invoice_id: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """
    指定されたIDの請求書情報を取得します。
    """
    db_invoice = crud.get_invoice(db, invoice_id=invoice_id)
    if db_invoice is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invoice not found",
        )
    return db_invoice

@router.put("/{invoice_id}", response_model=schemas.Invoice)
def update_invoice(
    invoice_id: str,
    invoice: schemas.InvoiceUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """
    指定されたIDの請求書情報を更新します。
    請求書作成権限が必要です。
    """
    if not current_user.create_invoice_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    db_invoice = crud.get_invoice(db, invoice_id=invoice_id)
    if db_invoice is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invoice not found",
        )
    if db_invoice.status != "draft":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only update draft invoices",
        )
    return crud.update_invoice(
        db=db,
        invoice_id=invoice_id,
        invoice=invoice,
        user_id=current_user.id,
    )

@router.post("/{invoice_id}/request-approval", response_model=schemas.Invoice)
def request_invoice_approval(
    invoice_id: str,
    approver_id: str,
    notes: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """
    指定されたIDの請求書を承認依頼します。
    請求書作成権限が必要です。
    """
    if not current_user.create_invoice_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    db_invoice = crud.get_invoice(db, invoice_id=invoice_id)
    if db_invoice is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invoice not found",
        )
    if db_invoice.status != "draft":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only request approval for draft invoices",
        )
    return crud.request_invoice_approval(
        db=db,
        invoice_id=invoice_id,
        approver_id=approver_id,
        notes=notes,
    )

@router.post("/{invoice_id}/approve", response_model=schemas.Invoice)
def approve_invoice(
    invoice_id: str,
    notes: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """
    指定されたIDの請求書を承認します。
    請求書承認権限が必要です。
    """
    if not current_user.approve_invoice_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    db_invoice = crud.get_invoice(db, invoice_id=invoice_id)
    if db_invoice is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invoice not found",
        )
    if db_invoice.status != "pending_approval":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only approve pending invoices",
        )
    return crud.approve_invoice(
        db=db,
        invoice_id=invoice_id,
        approver_id=current_user.id,
        notes=notes,
    )

@router.post("/{invoice_id}/issue", response_model=schemas.Invoice)
def issue_invoice(
    invoice_id: str,
    notes: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """
    指定されたIDの請求書を発行します。
    請求書作成権限が必要です。
    """
    if not current_user.create_invoice_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    db_invoice = crud.get_invoice(db, invoice_id=invoice_id)
    if db_invoice is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invoice not found",
        )
    if db_invoice.status != "approved":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only issue approved invoices",
        )
    return crud.issue_invoice(
        db=db,
        invoice_id=invoice_id,
        user_id=current_user.id,
        notes=notes,
    )

@router.post("/{invoice_id}/payments", response_model=schemas.Payment)
def register_payment(
    invoice_id: str,
    payment: schemas.PaymentCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """
    指定されたIDの請求書に支払いを登録します。
    収益管理権限が必要です。
    """
    if not current_user.manage_revenue_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    db_invoice = crud.get_invoice(db, invoice_id=invoice_id)
    if db_invoice is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invoice not found",
        )
    if db_invoice.status != "issued":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only register payments for issued invoices",
        )
    return crud.register_payment(
        db=db,
        invoice_id=invoice_id,
        payment=payment,
        user_id=current_user.id,
    ) 
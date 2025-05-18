from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ... import crud, models, schemas
from ...database import get_db
from ...auth import get_current_active_user

router = APIRouter()

# システム設定
@router.get("/system", response_model=schemas.SystemSetting)
def read_system_setting(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """
    システム設定を取得します。
    管理者権限が必要です。
    """
    if not current_user.admin_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    db_setting = crud.get_system_setting(db)
    if db_setting is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="System setting not found",
        )
    return db_setting

@router.post("/system", response_model=schemas.SystemSetting)
def create_system_setting(
    setting: schemas.SystemSettingCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """
    システム設定を作成します。
    管理者権限が必要です。
    """
    if not current_user.admin_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    db_setting = crud.get_system_setting(db)
    if db_setting:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="System setting already exists",
        )
    return crud.create_system_setting(db=db, setting=setting, user_id=current_user.id)

@router.put("/system", response_model=schemas.SystemSetting)
def update_system_setting(
    setting: schemas.SystemSettingUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """
    システム設定を更新します。
    管理者権限が必要です。
    """
    if not current_user.admin_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    db_setting = crud.get_system_setting(db)
    if db_setting is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="System setting not found",
        )
    return crud.update_system_setting(db=db, setting=setting, user_id=current_user.id)

# 税率設定
@router.get("/tax-rates", response_model=List[schemas.TaxRate])
def read_tax_rates(
    skip: int = 0,
    limit: int = 100,
    sort_by: str = "created_at",
    sort_order: str = "desc",
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """
    税率一覧を取得します。
    """
    return crud.get_tax_rates(
        db,
        skip=skip,
        limit=limit,
        sort_by=sort_by,
        sort_order=sort_order,
    )

@router.post("/tax-rates", response_model=schemas.TaxRate)
def create_tax_rate(
    tax_rate: schemas.TaxRateCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """
    新しい税率を作成します。
    管理者権限が必要です。
    """
    if not current_user.admin_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    return crud.create_tax_rate(db=db, tax_rate=tax_rate, user_id=current_user.id)

@router.put("/tax-rates/{tax_rate_id}", response_model=schemas.TaxRate)
def update_tax_rate(
    tax_rate_id: str,
    tax_rate: schemas.TaxRateUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """
    税率を更新します。
    管理者権限が必要です。
    """
    if not current_user.admin_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    db_tax_rate = crud.get_tax_rate(db, tax_rate_id=tax_rate_id)
    if db_tax_rate is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tax rate not found",
        )
    return crud.update_tax_rate(db=db, tax_rate_id=tax_rate_id, tax_rate=tax_rate)

# 支払い条件設定
@router.get("/payment-terms", response_model=List[schemas.PaymentTerm])
def read_payment_terms(
    skip: int = 0,
    limit: int = 100,
    sort_by: str = "created_at",
    sort_order: str = "desc",
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """
    支払い条件一覧を取得します。
    """
    return crud.get_payment_terms(
        db,
        skip=skip,
        limit=limit,
        sort_by=sort_by,
        sort_order=sort_order,
    )

@router.post("/payment-terms", response_model=schemas.PaymentTerm)
def create_payment_term(
    payment_term: schemas.PaymentTermCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """
    新しい支払い条件を作成します。
    管理者権限が必要です。
    """
    if not current_user.admin_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    return crud.create_payment_term(db=db, payment_term=payment_term, user_id=current_user.id)

@router.put("/payment-terms/{payment_term_id}", response_model=schemas.PaymentTerm)
def update_payment_term(
    payment_term_id: str,
    payment_term: schemas.PaymentTermUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """
    支払い条件を更新します。
    管理者権限が必要です。
    """
    if not current_user.admin_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    db_payment_term = crud.get_payment_term(db, payment_term_id=payment_term_id)
    if db_payment_term is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment term not found",
        )
    return crud.update_payment_term(db=db, payment_term_id=payment_term_id, payment_term=payment_term)

# メールテンプレート設定
@router.get("/email-templates", response_model=List[schemas.EmailTemplate])
def read_email_templates(
    skip: int = 0,
    limit: int = 100,
    sort_by: str = "created_at",
    sort_order: str = "desc",
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """
    メールテンプレート一覧を取得します。
    """
    return crud.get_email_templates(
        db,
        skip=skip,
        limit=limit,
        sort_by=sort_by,
        sort_order=sort_order,
    )

@router.post("/email-templates", response_model=schemas.EmailTemplate)
def create_email_template(
    template: schemas.EmailTemplateCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """
    新しいメールテンプレートを作成します。
    管理者権限が必要です。
    """
    if not current_user.admin_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    return crud.create_email_template(db=db, template=template, user_id=current_user.id)

@router.put("/email-templates/{template_id}", response_model=schemas.EmailTemplate)
def update_email_template(
    template_id: str,
    template: schemas.EmailTemplateUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """
    メールテンプレートを更新します。
    管理者権限が必要です。
    """
    if not current_user.admin_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    db_template = crud.get_email_template(db, template_id=template_id)
    if db_template is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email template not found",
        )
    return crud.update_email_template(db=db, template_id=template_id, template=template) 
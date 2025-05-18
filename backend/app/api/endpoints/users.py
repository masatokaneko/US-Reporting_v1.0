from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ... import crud, models, schemas
from ...database import get_db
from ...auth import get_current_active_user, get_current_admin_user

router = APIRouter()

@router.get("/", response_model=List[schemas.User])
def read_users(
    skip: int = 0,
    limit: int = 100,
    sort_by: str = "created_at",
    sort_order: str = "desc",
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin_user),
):
    """
    ユーザー一覧を取得します。
    管理者権限が必要です。
    """
    users = crud.get_users(db, skip=skip, limit=limit, sort_by=sort_by, sort_order=sort_order)
    return users

@router.post("/", response_model=schemas.User)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin_user),
):
    """
    新しいユーザーを作成します。
    管理者権限が必要です。
    """
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    return crud.create_user(db=db, user=user)

@router.get("/me", response_model=schemas.User)
def read_user_me(current_user: models.User = Depends(get_current_active_user)):
    """
    現在のユーザー情報を取得します。
    """
    return current_user

@router.get("/{user_id}", response_model=schemas.User)
def read_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin_user),
):
    """
    指定されたIDのユーザー情報を取得します。
    管理者権限が必要です。
    """
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return db_user

@router.put("/{user_id}", response_model=schemas.User)
def update_user(
    user_id: str,
    user: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin_user),
):
    """
    指定されたIDのユーザー情報を更新します。
    管理者権限が必要です。
    """
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return crud.update_user(db=db, user_id=user_id, user=user)

@router.put("/me", response_model=schemas.User)
def update_user_me(
    user: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    """
    現在のユーザー情報を更新します。
    """
    return crud.update_user(db=db, user_id=current_user.id, user=user) 
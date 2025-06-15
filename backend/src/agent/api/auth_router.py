from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from db import curd
from db.base import get_db
from schemas import user_schemas, token_schemas
from core.security import verify_password, create_access_token

router = APIRouter()


@router.post("/register", response_model=user_schemas.User)
def register_user(user: user_schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = curd.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="该邮箱已被注册")
    return curd.create_user(db=db, user=user)


@router.post("/login", response_model=token_schemas.Token)
def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: Session = Depends(get_db)
):
    # In OAuth2, the 'username' field of the form is used for the user identifier.
    # We are using email as the identifier.
    user = curd.get_user_by_email(db, email=form_data.username)

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="邮箱或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": user.email}
    )
    return {"access_token": access_token, "token_type": "bearer"}
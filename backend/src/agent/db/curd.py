import uuid
from sqlalchemy.orm import Session
from db.models import AiUser
from schemas import user_schemas
from core.security import get_password_hash


def get_user_by_email(db: Session, email: str):
    return db.query(AiUser).filter(AiUser.email == email).first()


def create_user(db: Session, user: user_schemas.UserCreate):
    # Generate a unique user_id
    user_id = uuid.uuid4().hex
    # Hash the password
    hashed_password = get_password_hash(user.password)

    db_user = AiUser(
        user_id=user_id,
        email=user.email,
        username=user.username,
        hashed_password=hashed_password,
        status=1  # Set status to online upon creation
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
from sqlalchemy import Column, BigInteger, String, Integer, DateTime, func
from .base import Base

class AiUser(Base):
    __tablename__ = "ai_user"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String(32), unique=True, index=True, nullable=False)
    email = Column(String(60), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    username = Column(String(255), nullable=False)
    status = Column(Integer, default=0) # 0:离线, 1:在线
    update_time = Column(DateTime, default=func.now(), onupdate=func.now())
    create_time = Column(DateTime, default=func.now())
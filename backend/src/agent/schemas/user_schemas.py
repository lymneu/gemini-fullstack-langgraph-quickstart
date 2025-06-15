from pydantic import BaseModel, EmailStr

# Schema for creating a user (from request body)
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    username: str

# Schema for reading user data (for response body)
# IMPORTANT: Never include password hash in responses
class User(BaseModel):
    user_id: str
    email: EmailStr
    username: str
    status: int

    class Config:
        from_attributes = True # Pydantic v2 replaces orm_mode
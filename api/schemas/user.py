from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)

class UserUpdate(BaseModel):
    full_name: str | None = None
    bio: str | None = None
    location: str | None = None
    phone_number: str | None = None

class UserOut(BaseModel):
    id: str
    email: EmailStr
    full_name: str | None = None
    bio: str | None = None
    location: str | None = None
    phone_number: str | None = None
    profile_image: str | None = None

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None

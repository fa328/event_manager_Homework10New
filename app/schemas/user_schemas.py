from pydantic import BaseModel, EmailStr, Field, validator, HttpUrl
from typing import Optional, List
from datetime import datetime
from enum import Enum
import uuid
import re

from app.utils.nickname_gen import generate_nickname


class UserRole(str, Enum):
    ANONYMOUS = "ANONYMOUS"
    AUTHENTICATED = "AUTHENTICATED"
    MANAGER = "MANAGER"
    ADMIN = "ADMIN"


def validate_url(url: Optional[str]) -> Optional[str]:
    """Helper function to validate URL format."""
    if url is None:
        return url
    url_regex = r'^https?:\/\/[^\s/$.?#].[^\s]*$'
    if not re.match(url_regex, url):
        raise ValueError('Invalid URL format')
    return url


class UserBase(BaseModel):
    email: EmailStr = Field(..., example="john.doe@example.com")
    nickname: Optional[str] = Field(None, min_length=3, pattern=r'^[\w-]+$', example=generate_nickname())
    first_name: Optional[str] = Field(None, example="John")
    last_name: Optional[str] = Field(None, example="Doe")
    bio: Optional[str] = Field(None, example="Experienced software developer specializing in web applications.")
    profile_picture_url: Optional[str] = Field(None, example="https://example.com/profiles/john.jpg")
    linkedin_profile_url: Optional[str] = Field(None, example="https://linkedin.com/in/johndoe")
    github_profile_url: Optional[str] = Field(None, example="https://github.com/johndoe")

    # Apply the URL validator to profile-related URLs
    _validate_urls = validator(
        'profile_picture_url', 'linkedin_profile_url', 'github_profile_url', pre=True, allow_reuse=True
    )(validate_url)

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    password: str = Field(..., example="Secure*1234", min_length=8, max_length=50)  # Updated password max length to 50


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    nickname: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    bio: Optional[str] = None
    profile_picture_url: Optional[HttpUrl] = None
    linkedin_profile_url: Optional[HttpUrl] = None
    github_profile_url: Optional[HttpUrl] = None

    # Validator for nickname to ensure it's alphanumeric, underscores, or hyphens
    @validator('nickname')
    def validate_nickname(cls, value):
        if value and not re.match(r'^[\w-]+$', value):
            raise ValueError('Nickname can only contain letters, numbers, underscores, and hyphens.')
        return value


class UserResponse(UserBase):
    id: uuid.UUID = Field(..., example=uuid.uuid4())
    role: UserRole = Field(default=UserRole.AUTHENTICATED, example="AUTHENTICATED")
    is_professional: Optional[bool] = Field(default=False, example=True)

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    email: str = Field(..., example="john.doe@example.com")
    password: str = Field(..., example="Secure*1234")


class ErrorResponse(BaseModel):
    error: str = Field(..., example="Not Found")
    details: Optional[str] = Field(None, example="The requested resource was not found.")


class UserListResponse(BaseModel):
    items: List[UserResponse] = Field(..., example=[{
        "id": uuid.uuid4(), 
        "nickname": generate_nickname(), 
        "email": "john.doe@example.com",
        "first_name": "John", 
        "last_name": "Doe", 
        "bio": "Experienced developer", 
        "role": "AUTHENTICATED",
        "profile_picture_url": "https://example.com/profiles/john.jpg", 
        "linkedin_profile_url": "https://linkedin.com/in/johndoe", 
        "github_profile_url": "https://github.com/johndoe"
    }])
    total: int = Field(..., example=100)
    page: int = Field(..., example=1)
    size: int = Field(..., example=10)

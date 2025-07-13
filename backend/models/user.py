from pydantic import BaseModel, Field, EmailStr, HttpUrl
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., min_length=8, description="User's password (will be hashed)")
    first_name: Optional[str] = Field(None, max_length=50, description="User's first name")
    last_name: Optional[str] = Field(None, max_length=50, description="User's last name")
    phone_number: Optional[str] = Field(None, max_length=15, pattern=r"^\+?[1-9]\d{1,14}$", description="Phone number (e.g., +1234567890)")
    role: str = Field("renter", description="User role: renter, lender, or admin")

    class Config:
        schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "securepassword123",
                "first_name": "John",
                "last_name": "Doe",
                "phone_number": "+1234567890",
                "role": "renter"
            }
        }

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = Field(None, description="User's email address")
    password: Optional[str] = Field(None, min_length=8, description="User's password (will be hashed)")
    first_name: Optional[str] = Field(None, max_length=50, description="User's first name")
    last_name: Optional[str] = Field(None, max_length=50, description="User's last name")
    phone_number: Optional[str] = Field(None, max_length=15, pattern=r"^\+?[1-9]\d{1,14}$", description="Phone number (e.g., +1234567890)")
    role: Optional[str] = Field(None, description="User role: renter, lender, or admin")

    class Config:
        json_schema_extra = {
            "example": {
                "email": "updated@example.com",
                "password": "newpassword123",
                "first_name": "Jane",
                "last_name": "Smith",
                "phone_number": "+9876543210",
                "role": "lender"
            }
        }

class UserResponse(BaseModel):
    id: int = Field(..., description="Unique user ID")
    email: EmailStr = Field(..., description="User's email address")
    first_name: Optional[str] = Field(None, description="User's first name")
    last_name: Optional[str] = Field(None, description="User's last name")
    phone_number: Optional[str] = Field(None, description="User's phone number")
    college_id_url: Optional[HttpUrl] = Field(None, description="URL to the user's college ID image")
    role: str = Field(..., description="User role: renter, lender, or admin")
    is_active: bool = Field(..., description="Whether the user account is active")

    class Config:
        orm_mode = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "email": "user@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "phone_number": "+1234567890",
                "college_id_url": "https://example.com/college_id/user_1_id.jpg",
                "role": "renter",
                "created_at": "2025-07-12T19:28:00",
                "updated_at": None,
                "is_active": True
            }
        }

class CollegeIdInput(BaseModel):
    college_id_url: HttpUrl = Field(..., description="URL to the college ID image (e.g., https://example.com/college_id.jpg)")

    class Config:
        json_schema_extra = {
            "example": {
                "college_id_url": "https://example.com/college_id/user_1_id.jpg"
            }
        }
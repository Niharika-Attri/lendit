from pydantic import BaseModel, Field, PositiveFloat
from typing import Optional, List
from datetime import datetime

class ItemCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Name of the item (e.g., 'Electric Kettle')")
    description: Optional[str] = Field(None, max_length=500, description="Detailed description of the item")
    price_per_hour: Optional[PositiveFloat] = Field(None, description="Rental price per hour")
    price_per_day: Optional[PositiveFloat] = Field(None, description="Rental price per day")
    category: Optional[str] = Field(None, max_length=50, description="Category (e.g., 'Electronics', 'Books')")
    location: str = Field(..., max_length=100, description="Pickup location (e.g., 'Hostel A, Room 101')")
    is_available: bool = Field(True, description="Whether the item is available for rent")
    images: Optional[List[str]] = Field(None, description="List of image URLs for the item")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Electric Kettle",
                "description": "1.5L electric kettle, perfect for hostel use",
                "price_per_hour": 1.5,
                "price_per_day": 5.0,
                "category": "Electronics",
                "location": "Hostel A, Room 101",
                "is_available": True,
                "images": ["https://example.com/kettle1.jpg"]
            }
        }

class ItemUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Name of the item (e.g., 'Electric Kettle')")
    description: Optional[str] = Field(None, max_length=500, description="Detailed description of the item")
    price_per_hour: Optional[PositiveFloat] = Field(None, description="Rental price per hour")
    price_per_day: Optional[PositiveFloat] = Field(None, description="Rental price per day")
    category: Optional[str] = Field(None, max_length=50, description="Category (e.g., 'Electronics', 'Books')")
    location: Optional[str] = Field(None, max_length=100, description="Pickup location (e.g., 'Hostel A, Room 101')")
    is_available: Optional[bool] = Field(None, description="Whether the item is available for rent")
    images: Optional[List[str]] = Field(None, description="List of image URLs for the item")

    class Config:
        schema_extra = {
            "example": {
                "name": "Electric Kettle",
                "description": "Updated 1.7L kettle",
                "price_per_hour": 2.0,
                "price_per_day": 6.0,
                "category": "Appliances",
                "location": "Hostel B, Room 202",
                "is_available": True,
                "images": ["https://example.com/kettle2.jpg"]
            }
        }

class ItemResponse(ItemCreate):
    id: int = Field(..., description="Unique item ID")

    class Config:
        orm_mode = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Electric Kettle",
                "description": "1.5L electric kettle, perfect for hostel use",
                "price_per_hour": 1.5,
                "price_per_day": 5.0,
                "category": "Electronics",
                "location": "Hostel A, Room 101",
                "is_available": True,
                "images": ["https://example.com/kettle1.jpg"]
            }
        }
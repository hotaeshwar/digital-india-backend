from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime

class ContactSubmission(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    phone: str = Field(..., min_length=10, max_length=15)
    email: EmailStr
    message: str = Field(..., min_length=10, max_length=1000)
    submitted_at: Optional[datetime] = None

    @validator('phone')
    def validate_phone(cls, v):
        phone = ''.join(filter(str.isdigit, v))
        if len(phone) != 10:
            raise ValueError('Phone number must be 10 digits')
        return phone